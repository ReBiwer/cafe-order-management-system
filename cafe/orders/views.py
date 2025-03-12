from django.http import Http404
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView

from orders import utils
from .forms import OrderForm, OrderItemFormSet
from .models import Order


class CreateOrder(TemplateView):
    template_name = "orders/create_order.html"

    def get_context_data(self, **kwargs):
        form = OrderForm()
        formset = OrderItemFormSet()
        data = super().get_context_data(**kwargs)
        data["form"] = form
        data["formset"] = formset
        return data

    def post(self, request: HttpRequest):
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        try:
            order_pk = utils.create_order(form, formset)
            if order_pk:
                return redirect(reverse("orders:detail", kwargs={"pk": order_pk}))
            raise Http404("Ошибка заполнения формы заказа")
        except Exception as e:
            raise Http404(f"Ошибка оформления заказа: {e}")


class ListOrders(ListView):
    model = Order
    template_name = "orders/list_orders.html"
    context_object_name = "orders"
