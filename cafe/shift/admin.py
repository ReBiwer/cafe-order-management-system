from django.contrib import admin

from orders.admin import OrderInline
from shift.models import Shift


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_display = [
        "date_open", "date_close", "total_orders", "active",
    ]
    readonly_fields = ["revenue", "date_close", "active"]

    def total_orders(self, obj):
        return obj.orders.count()

    def revenue(self, obj):
        if not obj.active:
            return obj.revenue

    def date_close(self, obj):
        if not obj.active:
            return obj.date_close

    total_orders.short_description = "Всего заказов"

