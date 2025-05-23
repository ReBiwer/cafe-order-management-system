from django.contrib import admin

from .models import Order, OrderItem, Dish


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "table_number", "status", "total_price", "created_at", "shift"
    ]


class OrderInline(admin.TabularInline):
    model = Order
    extra = 1
    fields = ["status", "created_at"]
    readonly_fields = ["total_price", "created_at"]

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

