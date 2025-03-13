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
    confirm = forms.BooleanField(
        label="Подтвердите удаление заказа",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Необходимо подтвердить удаление'}
    )

    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.pop('order_id', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('confirm'):
            raise forms.ValidationError("Подтвердите удаление")
        return cleaned_data


class OrderChangeForm(forms.Form):
    class Meta:
        model = Order
        fields = ["status"]
