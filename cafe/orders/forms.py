from django import forms
from django.forms import inlineformset_factory

from shift.models import Shift
from .models import Order
from .models import OrderItem


class OrderForm(forms.ModelForm):
    """
    Модель формы для создания заказа
    fields:
        table_number - номер стола

    Для добавления элементов заказа используется Formset описанный ниже
    """
    class Meta:
        model = Order
        fields = ["table_number"]

    def save(self, commit=True):
        current_shift = Shift.objects.filter(active=True).get()
        self.instance.shift = current_shift
        return super().save(commit)


class OrderItemForm(forms.ModelForm):
    """
    Модель формы для создания элементов заказа
    fields:
        dish - выбрать какой именно блюдо пойдет в заказ
        quantity - количество данной позиции
    """
    class Meta:
        model = OrderItem
        fields = ["dish", "quantity"]
        widgets = {
            'dish': forms.Select(attrs={'class': 'dish-select'}),
        }

# Formset для добавления элементов заказа.
# Основная модель OrderItem завязанная на модели Dish
OrderItemFormSet = inlineformset_factory(
    parent_model=Order, # родительская модель
    model=OrderItem,    # модель которая будет создаваться
    form=OrderItemForm, # форма которая будет использоваться для создания модели
    extra=1,            # стандартное кол-во форм для создания элементов
    can_delete=True,    # флаг для добавления возможности удалять новые формы
)

class OrderDeleteForm(forms.Form):
    """
    Модель формы для удаления заказа
    fields:
        confirm - простое подтверждение удаления для исключения ошибочного удаления
    """
    confirm = forms.BooleanField(
        label="Подтвердите удаление заказа",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        error_messages={'required': 'Необходимо подтвердить удаление'}
    )


class OrderChangeForm(forms.ModelForm):
    """
    Модель формы для изменения статуса заказа
    fields:
        status - статус заказа
    """
    class Meta:
        model = Order
        fields = ["status"]
