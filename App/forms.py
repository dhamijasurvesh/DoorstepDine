from django import forms
from django.contrib.auth.models import User 
from .models import (
    OfficeEmployee,
    TypeOfSubscription,
    Customer,
    Manager,
    Area,
    Restaurant,
    FoodItem,
    DeliveryAgent,
    Order,
    # Payment,
    # OrderStatus,
    # Feedback,
    Cart,
)


class RestaurantForm(forms.Form):
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        to_field_name="rest_id",  
        empty_label="Select a Restaurant",
        label="Restaurant" 
    )

from django import forms


class CustomerRegistrationForm(forms.ModelForm):
    cust_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = [
            'cust_id',
            'cust_password',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'email_id',
            'sub_id' 
        ]

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.set_password(self.cleaned_data["cust_password"])
        if commit:
            customer.save()
        return customer

class CustomerLoginForm(forms.Form):
    email_id = forms.EmailField()
    cust_password = forms.CharField(widget=forms.PasswordInput)
from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email_id', 'sub_id']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'sub_id': forms.Select(attrs={'class': 'form-control'}),
        }


