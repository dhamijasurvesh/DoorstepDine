from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# Create your models here.
class OfficeEmployee(models.Model):
    emp_name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=20, primary_key=True)
    phone_number = models.CharField(max_length=10)
    email_id = models.EmailField(max_length=150)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    hire_date = models.DateField()

    def __str__(self):
        return self.emp_name
    
class TypeOfSubscription(models.Model):
    sub_id = models.CharField(max_length=10, primary_key=True)
    validity_in_months = models.IntegerField()
    price = models.IntegerField()
    discount_in_perc = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.sub_id

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.validity_in_months < 2:
            raise ValidationError('Validity in months must be at least 2.')
        
class CustomerManager(BaseUserManager):
    def create_user(self, email_id, cust_password=None, **extra_fields):
        if not email_id:
            raise ValueError("The Email field must be set")
        email_id = self.normalize_email(email_id)
        user = self.model(email_id=email_id, **extra_fields)
        user.set_password(cust_password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email_id, cust_password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email_id, cust_password, **extra_fields)

class Customer(AbstractBaseUser, PermissionsMixin):
    cust_id = models.CharField(max_length=10, primary_key=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    email_id = models.EmailField(unique=True)
    sub_id = models.ForeignKey('TypeOfSubscription', on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email_id'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class Manager(models.Model):
    m_id = models.CharField(max_length=50, primary_key=True)
    m_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.m_id  

class Area(models.Model):
    area_id = models.CharField(max_length=50, primary_key=True)
    area_manager = models.ForeignKey('Manager', on_delete=models.CASCADE)
    def __str__(self):
        return f"Area ID: {self.area_id}, Manager ID: {self.area_manager.m_id}"
class Restaurant(models.Model):
    RESTAURANT_TYPE_CHOICES = [
        ('VEG', 'Veg'),
        ('NON-VEG', 'Non-Veg'),
        ('BOTHF', 'Both'),
    ]
    rest_id = models.CharField(max_length=10, primary_key=True)
    rest_name = models.CharField(max_length=100)
    r_type = models.CharField(max_length=7, choices=RESTAURANT_TYPE_CHOICES)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email_id = models.EmailField(max_length=100, blank=True, null=True)
    poc_name = models.CharField(max_length=100, blank=True, null=True)
    area = models.ForeignKey('Area', on_delete=models.CASCADE, blank=True, null=True)
    open_time = models.TimeField()
    close_time = models.TimeField()
    rest_rating = models.FloatField(default=0)
    def __str__(self):
        return self.rest_name
class FoodItem(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON-VEG', 'Non-Vegetarian'),
    ]
    product_id = models.CharField(max_length=10, primary_key=True)
    rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE) 
    product_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=700, choices=PRODUCT_TYPE_CHOICES)
    price = models.PositiveIntegerField()
    image_path = models.CharField(max_length=300)
    class Meta:
        db_table = 'food_items'  
    def __str__(self):
        return self.product_name

class DeliveryAgent(models.Model):
    d_id = models.CharField(max_length=10, primary_key=True)
    d_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    plate_number = models.CharField(max_length=10)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)

    class Meta:
        db_table = 'delivery_agents'  

    def __str__(self):
        return self.d_id



class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PREPARING', 'Preparing'),
        ('OUT FOR DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ] 
    order_id = models.CharField(max_length=10, primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount_in_perc = models.DecimalField(max_digits=4, decimal_places=2)
    order_amt = models.PositiveIntegerField()
    final_discounted_amt = models.FloatField()
    d_id = models.ForeignKey(DeliveryAgent, on_delete=models.CASCADE, null=True)
    rest_rating_given = models.FloatField(null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PREPARING')  
    feedback = models.CharField(max_length=500, null=True, blank=True) 

    class Meta:
        db_table = 'orders'  

    def clean(self):
        if self.rest_rating_given is not None and self.rest_rating_given > 5:
            raise ValidationError('Rating must be 5 or less.')

    def __str__(self):
        return self.order_id

class Cart(models.Model):
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'cart' 
        unique_together = (('cust_id', 'product_id'),)  

    def __str__(self):
        return f"Cart for {self.cust_id} - {self.product_id} (Quantity: {self.quantity})"