from django.contrib import admin

from .models import Order, OrderItem, Dish, Shift


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "table_number", "status", "total_price", "created_at", "shift"
    ]

from django.contrib import admin
from .models import Shift, Order

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

@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = [
        "date_open", "active", "total_orders"
    ]

    def total_orders(self, obj):
        return obj.orders.count()

    total_orders.short_description = "Всего заказов"
