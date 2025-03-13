from django import forms
from django.forms import inlineformset_factory

from .models import Order
from .models import OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number"]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["dish", "quantity"]
        widgets = {
            'dish': forms.Select(attrs={'class': 'dish-select'}),
        }


OrderItemFormSet = inlineformset_factory(
    parent_model=Order,
    model=OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)

class OrderDeleteForm(forms.Form):
    class Meta:
        model = Order
        fields = ["table_number"]
