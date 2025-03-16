from django.db import models
from django.urls import reverse

from .exceptions import CountShiftException

class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание блюда")
    available = models.BooleanField(default=True, verbose_name="Наличие блюда")

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'в ожидании'),
        ('ready', 'готово'),
        ('paid', 'оплачено'),
    ]

    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name="Общая стоимость"
    )
    shift = models.ForeignKey(
        'Shift',
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Смена",
        default=None
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def get_absolute_url(self):
        return reverse('orders:detail', kwargs={"pk": self.pk})

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Заказ"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='dishes_in_orders',
        verbose_name="Блюдо в заказе"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", default=0)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def save(self, *args, **kwargs):
        self.price = self.dish.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"


class Shift(models.Model):
    date_open = models.DateTimeField(auto_now=True, verbose_name="Дата открытия смены")
    active = models.BooleanField(default=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Выручка", null=True, blank=True)
    date_close = models.DateTimeField(verbose_name="Дата закрытия смены", null=True, blank=True)

    def save(self, *args, **kwargs):
        exist_shift = Shift.objects.filter(active=True).exists()
        if exist_shift:
            raise CountShiftException()
        return super().save(*args, **kwargs)
