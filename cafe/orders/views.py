from orders import utils
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpRequest
from django.http import Http404
from django.views.generic import TemplateView

from .forms import OrderForm, OrderItemFormSet



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
