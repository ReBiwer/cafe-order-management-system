from django.db import models

from shift.exceptions import CountShiftException


class Shift(models.Model):
    date_open = models.DateTimeField(auto_now_add=True, verbose_name="Дата открытия смены")
    active = models.BooleanField(default=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Выручка", null=True, blank=True)
    date_close = models.DateTimeField(verbose_name="Дата закрытия смены", null=True, blank=True)

