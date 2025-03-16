from django.contrib import admin

from .models import Order, OrderItem, Dish, Shift


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "table_number", "status", "total_price", "created_at",
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "order", "price", "quantity",
    ]

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        "name", "available",
    ]

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = [
        "date_open", "active"
    ]
