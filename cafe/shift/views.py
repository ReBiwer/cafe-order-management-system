from datetime import datetime

from django.db import transaction
from django.db.models import Sum
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from shift.exceptions import CountShiftException
from shift.models import Shift


class OpenShift(View):
    """
    Представление для открытия смены. Принимает только POST запрос
    """

    def post(self, request: HttpRequest):
        try:
            with transaction.atomic():
                Shift.objects.create()
                count_shifts = Shift.objects.filter(active=True).count()
                if count_shifts > 1:
                     raise CountShiftException
        except CountShiftException:
            return redirect(reverse("orders:exist_shift"))
        else:
            return redirect(reverse("orders:list"))


class CloseShift(View):
    """
    Представление для закрытия смены. Принимает только POST запрос
    """

    def post(self, request: HttpRequest):
        with transaction.atomic():
            open_shift: Shift = Shift.objects.filter(active=True).get()
            open_shift.active = False
            revenue = (
                Shift.objects
                .filter(pk=open_shift.pk, orders__status="paid")
                .select_related("orders")
                .aggregate(shift_revenue=Sum("orders__total_price"))
            )
            open_shift.revenue = revenue["shift_revenue"]
            open_shift.date_close = datetime.now()
            open_shift.save()
        return redirect(reverse("orders:list"))


class ShiftList(ListView):
    """
    Представление для отображения всех смен
    """
    template_name = "shift/list_shifts.html"
    context_object_name = "shifts"
    model = Shift


class ShiftDetail(DetailView):
    """
    Представление для отображения деталей смены
    """
    template_name = "shift/detail_shift.html"
    context_object_name = "shift"

    def get_queryset(self):
        return (Shift.objects
                .prefetch_related("orders")
                .prefetch_related("orders__items")
                .prefetch_related("orders__items__dish")
                )
