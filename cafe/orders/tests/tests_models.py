from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from shift.models import Shift
from orders.models import Order, OrderItem, Dish


class DishModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_dish = Dish.objects.create(
            name="Молочный коктейль",
            price=Decimal("120.99"),
        )

    def test_name_label(self):
        field_label = self.test_dish._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Название")

    def test_name_max_length(self):
        max_length = self.test_dish._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_price_label(self):
        field_label = self.test_dish._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "Цена")

    def test_price_max_digits(self):
        max_digits = self.test_dish._meta.get_field("price").max_digits
        self.assertEqual(max_digits, 10)

    def test_price_decimal_places(self):
        decimal_places = self.test_dish._meta.get_field("price").decimal_places
        self.assertEqual(decimal_places, 2)

    def test_description_label(self):
        field_label = self.test_dish._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Описание блюда")

    def test_description_null_blank(self):
        null_field = self.test_dish._meta.get_field("description").null
        blank = self.test_dish._meta.get_field("description").blank
        self.assertTrue(null_field)
        self.assertTrue(blank)

    def test_available_label(self):
        field_label = self.test_dish._meta.get_field("available").verbose_name
        self.assertEqual(field_label, "Наличие блюда")

    def test_available_default(self):
        default_value = self.test_dish._meta.get_field("available").default
        self.assertTrue(default_value)

class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shift = Shift.objects.create(active=True)
        cls.test_order = Order.objects.create(
            table_number=5,
            status="pending",
            shift=cls.shift
        )

    def test_table_number_label(self):
        field_label = self.test_order._meta.get_field("table_number").verbose_name
        self.assertEqual(field_label, "Номер стола")

    def test_status_label(self):
        field_label = self.test_order._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "Статус")

    def test_status_default(self):
        default_value = self.test_order._meta.get_field("status").default
        self.assertEqual(default_value, "pending")

    def test_status_max_length(self):
        max_length = self.test_order._meta.get_field("status").max_length
        self.assertEqual(max_length, 20)

    def test_total_price_label(self):
        field_label = self.test_order._meta.get_field("total_price").verbose_name
        self.assertEqual(field_label, "Общая стоимость")

    def test_total_price_default(self):
        default_value = self.test_order._meta.get_field("total_price").default
        self.assertEqual(default_value, 0)

    def test_shift_label(self):
        field_label = self.test_order._meta.get_field("shift").verbose_name
        self.assertEqual(field_label, "Смена")

    def test_created_at_label(self):
        field_label = self.test_order._meta.get_field("created_at").verbose_name
        self.assertEqual(field_label, "Дата создания")

    def test_str_representation(self):
        expected_str = f"Заказ #{self.test_order.id} (Стол 5)"
        self.assertEqual(str(self.test_order), expected_str)

    def test_get_absolute_url(self):
        expected_url = reverse('orders:detail', kwargs={"pk": self.test_order.pk})
        self.assertEqual(self.test_order.get_absolute_url(), expected_url)

class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.dish = Dish.objects.create(
            name="Пицца Маргарита",
            price=Decimal("12.50")
        )
        cls.shift = Shift.objects.create(active=True)
        cls.order = Order.objects.create(
            table_number=3,
            shift=cls.shift
        )
        cls.order_item = OrderItem.objects.create(
            order=cls.order,
            dish=cls.dish,
            quantity=2
        )

    def test_order_label(self):
        field_label = self.order_item._meta.get_field("order").verbose_name
        self.assertEqual(field_label, "Заказ")

    def test_dish_label(self):
        field_label = self.order_item._meta.get_field("dish").verbose_name
        self.assertEqual(field_label, "Блюдо в заказе")

    def test_price_label(self):
        field_label = self.order_item._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "Цена")

    def test_price_default(self):
        default_value = self.order_item._meta.get_field("price").default
        self.assertEqual(default_value, 0)

    def test_quantity_label(self):
        field_label = self.order_item._meta.get_field("quantity").verbose_name
        self.assertEqual(field_label, "Количество")

    def test_quantity_default(self):
        default_value = self.order_item._meta.get_field("quantity").default
        self.assertEqual(default_value, 1)

    def test_price_auto_calculation(self):
        """Проверка автоматического расчета цены при создании"""
        self.assertEqual(self.order_item.price, Decimal("12.50"))

    def test_price_update_on_dish_change(self):
        """Проверка обновления цены при изменении блюда"""
        new_dish = Dish.objects.create(
            name="Новое блюдо",
            price=Decimal("15.00")
        )
        self.order_item.dish = new_dish
        self.order_item.save()
        self.assertEqual(self.order_item.price, Decimal("15.00"))

    def test_str_representation(self):
        expected_str = f"Пицца Маргарита x2"
        self.assertEqual(str(self.order_item), expected_str)
