from django.db import models
from django.urls import reverse

from shift.models import Shift


class Dish(models.Model):
    """
    Модель блюда. Данная модель представляет собой блюда, которые имеются в кафе.
    Любые операции с ними можно делать только в админ панели
    fields:
        name - название блюда
        price - цена блюда
        description - описание блюда
        available - наличие блюда
    """
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(null=True, blank=True, verbose_name="Описание блюда")
    available = models.BooleanField(default=True, verbose_name="Наличие блюда")

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    """
    Модель заказа. Данная модель представляет собой заказа. Создать заказ можно только при открытой смене.
    fields:
        table_number - номер столика к которому относится данный заказ
        status - статус заказа (в ожидании, готово, оплачено)
        total_price - общая стоимость заказа. Высчитывается автоматически при удалении или добавлении блюд
        shift - смена в которую был создан данный заказ (привязывается при создании заказа)
        created_at - время создания заказа

        items - related_name связанное внешним ключом с моделью OrderItem
    """
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
        Shift,
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
    """
    Модель элемента заказа. Данная модель представляет элемент заказа.
    Связана с блюдом на основании которого был добавлен данная позиция.
    fields:
        order - внешний ключ связанный с заказом (related_name - items)
        dish - внешний ключ связанный с блюдом в кафе (related_name - dishes_in_orders)
        price - цена позиции заказа
        quantity - количество в заказе
    """
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
