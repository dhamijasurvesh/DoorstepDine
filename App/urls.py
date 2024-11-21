from django.urls import path
# from .views import login_view, logout_view
from . import views
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),  
    path('about/', views.about, name='about'),  
    path('restaurants/', views.restaurant, name='restaurant'),
    path('change_rating/<str:order_id>/', views.change_rating, name='change_rating'),
    # path('menu/', views.menu, name='menu'),
    path('update_feedback/<str:order_id>/', views.update_feedback, name='update_feedback'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'), 
    # path('mycart/', views.my_cart, name='my_cart'), 
    path('myaccount/', views.myaccount, name='myaccount'),  
    path('logout/',views.customer_logout, name='logout'),  
    path('orders/', views.orders, name='orders'),
    path('order_successful/', views.order_successful, name='order_successful'),
    # path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('confirm_order/', views.confirm_order, name='confirm_order'),
    path('update_cart_quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'), 
    # path('restaurant-autocomplete/', RestaurantAutocomplete.as_view(), name='restaurant-autocomplete'),
 
]
