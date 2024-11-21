from django.contrib import admin
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


admin.site.register(OfficeEmployee)
admin.site.register(TypeOfSubscription)
admin.site.register(Customer)
admin.site.register(Manager)
admin.site.register(Area)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(DeliveryAgent)
admin.site.register(Order)
# admin.site.register(Payment)
# admin.site.register(OrderStatus)
# admin.site.register(Feedback)
admin.site.register(Cart)
