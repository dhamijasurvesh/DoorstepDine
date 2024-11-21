from django.shortcuts import render
from .forms import RestaurantForm
from .models import Restaurant, FoodItem,Order
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import Customer,FoodItem
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, Restaurant


def change_rating(request, order_id):
    if request.method == "POST":
        new_rating = float(request.POST.get("new_rating"))
        order = get_object_or_404(Order, order_id=order_id)
        order.rest_rating_given = new_rating 
        order.save()
        rest_id = order.product_id.rest_id 
        average_rating = Order.objects.filter(product_id=order.product_id).aggregate(
            avg_rating=Avg('rest_rating_given')
        )['avg_rating']
        if average_rating is not None:
            rest_id.rest_rating = average_rating
            rest_id.save()

        messages.success(request, "Rating updated successfully!")
        return redirect('orders')

def orders(request):
    if request.user.is_authenticated:
       
        orders = Order.objects.filter(cust_id=request.user)
    else:
        orders = []
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)

def update_feedback(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id)
        feedback = request.POST.get('feedback', '')
        order.feedback = feedback
        order.save()
        return redirect('orders')
    
def order_successful(request):
    return render(request, 'order_successful.html')

from django.shortcuts import render, redirect
from .forms import CustomerRegistrationForm  
from .models import TypeOfSubscription

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    subscriptions = TypeOfSubscription.objects.all()
    return render(request, 'register.html', {'form': form, 'subscriptions': subscriptions})

def customer_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email_id = form.cleaned_data['email_id']
            cust_password = form.cleaned_data['cust_password']
            user = authenticate(request, email_id=email_id, password=cust_password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = CustomerLoginForm()
    return render(request, 'login.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
def home(request):
    return render(request, 'home.html')

def restaurant(request):
    items = None
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            selected_restaurant = form.cleaned_data['restaurant']
            items = FoodItem.objects.filter(rest_id=selected_restaurant) 
    else:
        form = RestaurantForm()
    return render(request, 'restaurants.html', {'items': items, 'form': form})

def cart(request):
    return render(request, 'cart.html')
def myaccount(request):
    return render(request, 'myaccount.html')
def customer_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import redirect, get_object_or_404
from .models import FoodItem, Cart
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        customer = request.user
        food_item = get_object_or_404(FoodItem, pk=product_id)    
        cart_item, created = Cart.objects.get_or_create(
            cust_id=customer, 
            product_id=food_item,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return redirect('cart')  
    else:
        return HttpResponse("Invalid request method", status=400)
    

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))  
        item = get_object_or_404(Cart, id=item_id) 

        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, 'Quantity updated successfully!')
        else:
            messages.error(request, 'Quantity must be at least 1.')

        return redirect('cart')
    else:
        return redirect('cart')  


from .models import Cart
from django.shortcuts import render
from decimal import Decimal
from .models import Cart, TypeOfSubscription
from django.http import JsonResponse
import stripe
from django.conf import settings
from decimal import Decimal
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
from decimal import Decimal
import stripe
import os
stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')

from .models import Restaurant


from decimal import Decimal
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from .models import Cart
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
import stripe
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from decimal import Decimal
import random
import string

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def generate_order_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@csrf_exempt
def checkout(request):
    customer = request.user
    cart_items = Cart.objects.filter(cust_id=customer)
    total_price = sum(item.product_id.price * item.quantity for item in cart_items)
    discount_percentage = customer.sub_id.discount_in_perc if customer.sub_id else 0  
    discount_amount = total_price * (Decimal(discount_percentage) / 100)
    discounted_total = total_price - discount_amount

    if request.method == 'POST':
        
        intent = stripe.PaymentIntent.create(
            amount=int(discounted_total * 100), 
            currency='inr',
            metadata={'cust_id': customer.cust_id}
        )

        return JsonResponse({'client_secret': intent.client_secret})

   
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_percentage': discount_percentage,
        'discount_amount': discount_amount,
        'discounted_total': discounted_total,
        'stripe_public_key': settings.STRIPE_TEST_PUBLISHABLE_KEY,
    }
    return render(request, 'checkout.html', context)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Cart
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@csrf_exempt
def confirm_order(request):
    if request.method == 'POST':
        customer = request.user
        cart_items = Cart.objects.filter(cust_id=customer)
        discount_percentage = customer.sub_id.discount_in_perc if customer.sub_id else 0  
        discounted_total = sum(item.product_id.price * item.quantity for item in cart_items) * (1 - (discount_percentage / 100))
        order_details = create_order(customer, cart_items, discount_percentage, discounted_total)
        cart_items.delete()
        send_order_confirmation_email(customer, order_details)
        return JsonResponse({'success': True, 'message': 'Order created successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def send_order_confirmation_email(customer, order_details):
    subject = 'Order Confirmation'
    message = render_to_string('order_confirmation_email.html', {
        'customer_name': f"{customer.first_name} {customer.last_name}",
        'order_details': order_details,
    })
    from_email = 'dhamijasurvesh@gmail.com' 
    to_email = customer.email_id
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            html_message=message,
        )
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")

def create_order(customer, cart_items, discount_percentage, discounted_total):
    order_details = [] 
    for item in cart_items:
        order = Order.objects.create(
            order_id=generate_order_id(),
            cust_id=customer,
            product_id=item.product_id,
            quantity=item.quantity,
            discount_in_perc=discount_percentage,
            order_amt=item.product_id.price * item.quantity,
            final_discounted_amt=discounted_total,
            status='PREPARING'
        )
        order_details.append({
            'product_name': item.product_id.product_name, 
            'quantity': item.quantity,
            'order_amt': item.product_id.price * item.quantity,
            'discounted_amt': discounted_total
        })
    return order_details

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from templated_email import send_templated_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from post_office import mail  
import logging

logger = logging.getLogger(__name__)
  
def delete_from_cart(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Cart, id=item_id)  
        item.delete()  
        return redirect('cart') 


def cart_view(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(cust_id=request.user)  
        total_price = sum(item.product_id.price * item.quantity for item in cart_items)  
        context = {
            'cart_items': cart_items,
            'total_price': total_price,
        }
        return render(request, 'cart.html', context)
    else:
        return redirect('login')  
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CustomerForm  

@login_required
def myaccount(request): 
    customer = request.user 
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save() 
            return redirect('myaccount')  
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'myaccount.html', {'form': form, 'customer': customer})