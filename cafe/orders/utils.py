from django.db import transaction

from .forms import OrderForm, OrderItemFormSet


def create_order(order_form: OrderForm, order_items_formset: OrderItemFormSet) -> int | None:
    """
    Функция для создания заказа на основе данных с OrderForm и OrderItemFormSet
    :param order_form: форма с данными нового заказа
    :param order_items_formset: набор форм для создания позиций заказа
    :return: при успешном создании заказа возвращает id заказа, в случае ошибки возвращает None
    """
    if order_form.is_valid() and order_items_formset.is_valid():
        with transaction.atomic():
            order = order_form.save()
            items_order = order_items_formset.save(commit=False)
            for item in items_order:
                item.order = order
                item.save()
        return order.pk
    return None