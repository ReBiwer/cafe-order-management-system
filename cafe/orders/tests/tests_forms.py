from django.test import TestCase
from django import forms

from orders.models import Order, OrderItem
from orders.forms import OrderForm, OrderItemForm, OrderItemFormSet, OrderDeleteForm, OrderChangeForm


class OrderFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Инициализация тестовых данных для формы заказа"""
        cls.form = OrderForm()

    def test_model_to_form(self):
        """Проверка привязки формы к модели Order"""
        self.assertEqual(self.form.Meta.model, Order)

    def test_field_form(self):
        """Проверка отображаемых полей формы"""
        self.assertEqual(self.form.Meta.fields, ["table_number"])


class OrderItemFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Инициализация тестовых данных для формы элемента заказа"""
        cls.form = OrderItemForm()

    def test_model_to_form(self):
        """Проверка привязки формы к модели OrderItem"""
        self.assertEqual(self.form.Meta.model, OrderItem)

    def test_fields_form(self):
        """Проверка наличия обязательных полей в форме"""
        self.assertIn("dish", self.form.Meta.fields)
        self.assertIn("quantity", self.form.Meta.fields)

    def test_widget_form(self):
        """Проверка корректности виджета для поля dish"""
        widgets = self.form.Meta.widgets
        self.assertIn('dish', widgets)
        self.assertIsInstance(widgets["dish"], forms.Select)
        self.assertIn(widgets["dish"].attrs["class"], "dish-select")


class OrderItemFormSetTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Инициализация тестовых данных для формсета элементов заказа"""
        cls.formset = OrderItemFormSet()

    def test_model(self):
        """Проверка привязки формсета к модели OrderItem"""
        self.assertEqual(self.formset.model, OrderItem)

    def test_form_model(self):
        """Проверка использования правильной формы в формсете"""
        self.assertIsInstance(self.formset.forms[0], OrderItemForm)

    def test_can_delete(self):
        """Проверка возможности удаления элементов в формсете"""
        self.assertTrue(self.formset.can_delete)


class OrderDeleteFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = OrderDeleteForm()

    def test_form_fields(self):
        """Проверяем наличие поля confirm"""
        self.assertIn('confirm', self.form.fields)

    def test_confirm_label(self):
        """Проверяем метку поля"""
        field_label = self.form.fields['confirm'].label
        self.assertEqual(field_label, "Подтвердите удаление заказа")

    def test_confirm_required(self):
        """Проверяем обязательность поля"""
        field_required = self.form.fields['confirm'].required
        self.assertTrue(field_required)

    def test_confirm_widget(self):
        """Проверяем виджет и его атрибуты"""
        widget = self.form.fields['confirm'].widget
        self.assertIsInstance(widget, forms.CheckboxInput)
        self.assertEqual(widget.attrs.get('class'), 'form-check-input')

    def test_error_messages(self):
        """Проверяем кастомные сообщения об ошибках"""
        form = OrderDeleteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['confirm'], ['Необходимо подтвердить удаление'])


class OrderChangeFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = OrderChangeForm()

    def test_model_to_form(self):
        """Проверяем привязку к модели"""
        self.assertEqual(self.form.Meta.model, Order)

    def test_form_fields(self):
        """Проверяем доступные поля формы"""
        self.assertEqual(self.form.Meta.fields, ["status"])

    def test_status_choices(self):
        """Проверяем доступные варианты статусов"""
        status_field = self.form.fields['status']
        self.assertIsInstance(status_field.widget, forms.Select)
        self.assertEqual(
            status_field.choices,
            [
                ('pending', 'в ожидании'),
                ('ready', 'готово'),
                ('paid', 'оплачено'),
            ]
        )

    def test_valid_status_change(self):
        """Проверяем валидацию допустимых статусов"""
        valid_data = {'status': 'ready'}
        form = OrderChangeForm(data=valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_status_change(self):
        """Проверяем валидацию недопустимых статусов"""
        invalid_data = {'status': 'invalid_status'}
        form = OrderChangeForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)
