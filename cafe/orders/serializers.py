from adrf.serializers import ModelSerializer
from rest_framework import serializers

from .models import Order, OrderItem, Dish


class DishSerializer(ModelSerializer):
    """
    Сериализатор для модели Dish
    """
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
        read_only_fields = ["id"]


class OrderSerializer(ModelSerializer):
    """
    Сериализатор для заказа
    fields:
        order_items - список позиций заказа
        status - статус заказа
        url - генерируемое поле ссылки на заказ
    """
    order_items = OrderItemSerializer(many=True, source="items")
    status = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "table_number", "status", "total_price", "order_items", "url"]
        read_only_fields = ["id"]

    def get_url(self, obj: Order):
        return obj.get_absolute_url()


    def create(self, validated_data):
        """
        Переопределенный метод создания модели Order с созданием OrderItem
        :param validated_data: валидные данные
        :return:
        """
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                dish=item_data['dish'],
                quantity=item_data['quantity']
            )
        return order

    def update(self, instance, validated_data):
        """
        Переопределенный метод обновления модели Order и связанных с ним OrderItem
        :param instance: экземпляр модели, который обновляется
        :param validated_data: валидные данные заказа
        :return:
        """
        items_data = validated_data.pop('order_items', [])

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
                dish_orderitem = Dish.objects.get(id=item_data['dish'])
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