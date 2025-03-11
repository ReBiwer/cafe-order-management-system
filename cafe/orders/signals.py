from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem, Order

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance: OrderItem, **kwargs):
    order: Order = instance.order
    total = sum(item.dish.price * item.quantity for item in order.items.all())
    order.total_price = total
    order.save(update_fields=['total_price'])
