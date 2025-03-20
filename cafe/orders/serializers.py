from adrf.serializers import ModelSerializer
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers

from shift.models import Shift
from .models import Order, OrderItem, Dish


class DishSerializer(ModelSerializer):
    """
    Сериализатор для модели Dish
    """
    id = serializers.IntegerField()
    class Meta:
        model = Dish
        fields = ["id", "name", "description"]


class OrderItemSerializer(ModelSerializer):
    """
    Сериализатор для позиции заказа
    """
    dish = DishSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "price", "quantity", "dish"]
        # read_only_fields = ["id"]


class ShiftSerializer(ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Shift
        fields = ["id"]
        read_only_fields = ["id"]


class OrderSerializer(ModelSerializer):
    """
    Сериализатор для заказа
    fields:
        items - список позиций заказа
        status - статус заказа
        url - генерируемое поле ссылки на заказ
    """
    items = OrderItemSerializer(many=True)
    status = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    shift = ShiftSerializer()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "table_number", "shift", "status", "total_price", "items", "url"]
        read_only_fields = ["id", "url"]

    def get_url(self, obj: Order):
        return obj.get_absolute_url()


    def create(self, validated_data):
        """
        Переопределенный метод создания модели Order с созданием OrderItem
        :param validated_data: валидные данные
        :return:
        """
        items_data = validated_data.pop('items')
        shift_pk = validated_data.pop('shift')
        try:
            with transaction.atomic():
                active_shift = Shift.objects.get(pk=shift_pk["id"])
                order = Order(**validated_data, shift=active_shift)
                order.save()
                items = []
                for item_data in items_data:
                    item = OrderItem(
                        order=order,
                        dish=Dish.objects.get(pk=item_data['dish']['id']),
                        quantity=item_data['quantity']
                    )
                    items.append(item)
                OrderItem.objects.bulk_create(items)
        except ObjectDoesNotExist as e:
            raise Http404(e)
        else:
            return order

    def update(self, instance, validated_data):
        """
        Переопределенный метод обновления модели Order и связанных с ним OrderItem
        :param instance: экземпляр модели, который обновляется
        :param validated_data: валидные данные заказа
        :return:
        """
        items_data = validated_data.pop('items', [])
        with transaction.atomic():
            # Обновление полей заказа
            instance.table_number = validated_data.get('table_number', instance.table_number)
            instance.status = validated_data.get('status', instance.status)
            instance.save()

            # Текущие элементы заказа
            current_items = {item.id: item for item in instance.items.all()}
            requested_ids = set()

            # Обработка элементов
            for item_data in items_data:
                item_id = item_data.get('id')

                # Обновление существующего элемента
                if item_id and item_id in current_items:
                    item = current_items[item_id]
                    item.dish = item_data['dish']
                    item.quantity = item_data['quantity']
                    item.save()  # Автоматически обновит price
                    requested_ids.add(item_id)

                # Создание нового элемента
                else:
                    dish_orderitem = Dish.objects.get(pk=item_data['dish']["id"])
                    OrderItem.objects.create(
                        order=instance,
                        dish=dish_orderitem,
                        quantity=item_data['quantity']
                    )

            # Удаление отсутствующих в запросе элементов
            for item_id in current_items:
                if item_id not in requested_ids:
                    current_items[item_id].delete()

        return instance