from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.http import Http404
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView

from orders import utils
from shift.models import Shift
from .forms import OrderForm, OrderItemFormSet, OrderDeleteForm, OrderChangeForm
from .models import Order
from .serializers import OrderSerializer



class CreateOrder(TemplateView):
    """
    Представление для создания заказов и добавления позиций к заказу
    """
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
                return redirect(reverse("orders:list"))
            raise Http404("Ошибка заполнения формы заказа")
        except Exception as e:
            raise Http404(f"Ошибка оформления заказа: {e}")


class ListOrders(ListView):
    """
    Представление для отображения информации о всех заказах в текущей смене
    """
    template_name = "orders/list_orders.html"
    context_object_name = "shift"

    def get_queryset(self):
        try:
            queryset = get_object_or_404(
                Shift.objects
                .filter(active=True)
                .prefetch_related("orders")
                .prefetch_related("orders__items")
                .prefetch_related("orders__items__dish")
            )
        except Exception as e:
            queryset = None
        return queryset


class DetailOrder(DetailView):
    """
    Представления для отображения деталей заказа
    """
    model = Order
    template_name = "orders/detail_order.html"
    context_object_name = "order"


class DeleteOrder(DeleteView):
    """
    Представление для удаления заказа
    """
    form_class = OrderDeleteForm
    template_name = "orders/delete_order.html"
    context_object_name = "order"
    success_url = reverse_lazy("orders:list")

    def get_queryset(self):
        order_id = self.kwargs.get("pk")
        return (Order.objects
                .filter(pk=order_id)
                .prefetch_related("items")
                .prefetch_related("items__dish")
                )


class ChangeStatusOrder(UpdateView):
    """
    Представление для изменения статуса заказа
    """
    form_class = OrderChangeForm
    template_name = "orders/change_status_order.html"
    context_object_name = "order"

    def get_queryset(self):
        order_id = self.kwargs.get("pk")
        return (Order.objects
                .filter(pk=order_id)
                .prefetch_related("items")
                .prefetch_related("items__dish")
                )

    def get_success_url(self):
        order_id = self.kwargs.get("pk")
        return reverse("orders:detail", kwargs={"pk": order_id})


class APIOrder(ModelViewSet):
    """
    ModelViewSet для взаимодействия с заказами через DRF
    """
    queryset = (Order.objects
                .prefetch_related("items")
                .prefetch_related("items__dish")
                .all())
    serializer_class = OrderSerializer


class SearchAPIOrder(APIView):
    """
    API представление для поиска заказа.
    Предназначено для поисковой строки.
    Взаимодействие на фронте происходит через JS скрипт
    """

    def get(self, request: Request):
        value_search = request.query_params.get('value_search')
        STATUS_MAPPING = {
            'в ожидании': 'pending',
            'ожидании': 'pending',
            'готово': 'ready',
            'готов': 'ready',
            'оплачено': 'paid'
        }
        queryset = None
        try:
            if not value_search.isdigit():
                if value_search.lower() in STATUS_MAPPING:
                    status_order = STATUS_MAPPING.get(value_search.lower())
                    queryset = (
                        Order.objects
                        .filter(status=status_order)
                        .prefetch_related("items")
                        .prefetch_related("items__dish")
                    ).all()
                elif value_search.lower() in STATUS_MAPPING.keys():
                    queryset = (
                        Order.objects
                        .filter(status=value_search)
                        .prefetch_related("items")
                        .prefetch_related("items__dish")
                    ).all()
            else:
                queryset = (
                    Order.objects
                    .filter(table_number=int(value_search))
                    .prefetch_related("items")
                    .prefetch_related("items__dish")
                ).all()
            if queryset:
                result = OrderSerializer(queryset, many=True)
                return Response(result.data)
            else:
                raise Http404("No data found")
        except Exception as e:
            raise Http404("No data found")
