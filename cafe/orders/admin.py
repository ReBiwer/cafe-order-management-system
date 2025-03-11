from django.contrib import admin

from .models import Order, OrderItem, Dish


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "table_number", "status", "total_price", "created_at",
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order", "dish_name", "price", "quantity", "status"
    ]

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        "name", "available",
    ]
