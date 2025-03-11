from django import forms
from django.forms import inlineformset_factory

from cafe.orders.models import Order
from cafe.orders.models import OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["dish", "quantity"]


OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=False,
)
