from django.db import models


class Shift(models.Model):
    """
    Модель рабочей смены. Данная модель представляет собой рабочую смену. Без нее нет возможности создать новый заказ.
    Модель связана related_name с экземплярами модели Order через "orders"
    fields:
        date_open - дата открытия смены (создает автоматически при создании экземпляра)
        active - статус смены (активна/не активна)
        revenue - выручка (считается при закрытии смены с оплаченных заказов)
        date_close - дата закрытия смены

        orders -
    """
    date_open = models.DateTimeField(auto_now_add=True, verbose_name="Дата открытия смены")
    active = models.BooleanField(default=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Выручка", null=True, blank=True)
    date_close = models.DateTimeField(verbose_name="Дата закрытия смены", null=True, blank=True)

    def __str__(self):
        return f"Дата откртытия смены {self.date_open}"
