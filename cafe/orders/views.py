from datetime import datetime

from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from django.http import Http404
from django.http import HttpRequest
from django.shortcuts import redirect
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, DeleteView, UpdateView, View

from orders import utils
from .exceptions import CountShiftException
from .forms import OrderForm, OrderItemFormSet, OrderDeleteForm, OrderChangeForm
from .models import Order, Shift
from .serializers import OrderSerializer


class OpenShift(View):

    def post(self, request: HttpRequest):
        try:
            Shift.objects.create()
        except CountShiftException:
            return redirect(reverse("orders:exist_shift"))
        else:
            return redirect(reverse("orders:list"))


class CloseShift(View):

    def post(self, request: HttpRequest):
        with transaction.atomic():
            open_shift: Shift = Shift.objects.filter(active=True).get()
            open_shift.active = False
            revenue = (
                Shift.objects
                .filter(pk=open_shift.pk)
                .select_related("orders")
                .aggregate(shift_revenue=Sum("orders__total_price"))
            )
            open_shift.revenue = revenue["shift_revenue"]
            open_shift.date_close = datetime.now()
            open_shift.save()
        return redirect(reverse("orders:list"))


class ShiftList(ListView):
    template_name = "shift/list_shifts.html"
    context_object_name = "shifts"
    model = Shift


class ShiftDetail(DetailView):
    template_name = "shift/detail_shift.html"
    context_object_name = "shift"

    def get_queryset(self):
        return (Shift.objects
                .prefetch_related("orders")
                .prefetch_related("orders__items")
                .prefetch_related("orders__items__dish")
                )

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
                return redirect(reverse("orders:list"))
            raise Http404("Ошибка заполнения формы заказа")
        except Exception as e:
            raise Http404(f"Ошибка оформления заказа: {e}")


class ListOrders(ListView):
    template_name = "orders/list_orders.html"
    context_object_name = "shift"

    def get_queryset(self):
        queryset = (
            Shift.objects
            .prefetch_related("orders")
            .prefetch_related("orders__items")
            .prefetch_related("orders__items__dish")
            .get()
        )
        return queryset


class DetailOrder(DetailView):
    model = Order
    template_name = "orders/detail_order.html"
    context_object_name = "order"


class DeleteOrder(DeleteView):
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
    queryset = (Order.objects
                .prefetch_related("items")
                .prefetch_related("items__dish")
                .all())
    serializer_class = OrderSerializer


class SearchAPIOrder(APIView):

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
