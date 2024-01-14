import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Order, OrderItem, OrderCancellation, OrderItemCancellation

# Define a logger for this module
logger = logging.getLogger(__name__)


class InlineOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'variation_ids', 'product_id', 'item_price', 'quantity', 'is_item_cancelled',
                  'created_at', 'modified_at']
        extra_kwargs = {'is_item_cancelled': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_items', 'delivery_address_id', 'order_delivery_status', 'order_total_price',
                  'delivery_charge', 'order_payment_status', 'is_order_cancelled', 'created_at', 'modified_at']
        extra_kwargs = {
            'order_total_price': {'required': False},
            'is_order_cancelled': {'read_only': True}
        }

    def get_order_items(self, instance):
        # Filter only the order items where is_item_canceled is False
        order_items = instance.order_items.filter(is_item_cancelled=False)

        # Serialize the filtered order items
        serializer = InlineOrderItemSerializer(order_items, many=True)
        return serializer.data


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'order_delivery_status']


class InlineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_delivery_status']


class OrderItemSerializer(serializers.ModelSerializer):
    order = InlineOrderSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'variation_ids', 'product_id', 'item_price', 'quantity', 'is_item_cancelled',
                  'created_at', 'modified_at']
        extra_kwargs = {'is_item_cancelled': {'read_only': True}}


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'variation_ids', 'product_id', 'item_price', 'quantity', 'is_item_cancelled', 'created_at', ]
        extra_kwargs = {'is_item_cancelled': {'read_only': True}}

    def create(self, validated_data):
        order_id = self.context['order_id']

        try:
            # check whether the order_id in the url params exists
            order = Order.objects.only('id').get(id=order_id)
        except Order.DoesNotExist:
            # Handle the case where the order does not exist
            logger.error(f"Order with id={order_id} does not exist")
            raise ValueError("Order with id={} does not exist".format(order_id))

        logger.info(f"OrderItem created for Order {order.id}")
        return OrderItem.objects.create(order_id=order.id, **validated_data)


class OrderCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCancellation
        fields = ['id', 'order_cancel_reason', 'created_at']
        extra_kwargs = {'order_cancel_reason': {'required': False}}

    def validate(self, attrs):
        order_id = self.context['order_id']
        try:
            order = Order.objects.get(id=order_id)
            if order.is_order_cancelled:
                return serializers.ValidationError('This order has already been cancelled!')
            if order.order_delivery_status in ["Shipped", "Delivered"]:
                return serializers.ValidationError("You can't cancel your order after it has been shipped or delivered")
        except Order.DoesNotExist:
            return serializers.ValidationError("No order exists with given ID!")
        if len(attrs['order_cancel_reason']) < 20:
            return serializers.ValidationError("Reason must be at least 20 characters")
        return attrs

    def create(self, validated_data):
        order_id = self.context['order_id']
        order = get_object_or_404(Order, id=order_id)
        order.is_order_cancelled = True
        order.save()

        logger.info(f"Order with {order_id} cancelled successfully")
        return OrderCancellation.objects.create(order_id=order_id, **validated_data)


class OrderItemCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItemCancellation
        fields = ['id', 'order_item_cancel_reason']
        extra_kwargs = {'order_item_cancel_reason': {'required': False}}

    def validate(self, attrs):
        order_item_id = self.context['order_item_id']
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            order = Order.objects.get(id=order_item.order_id)
            if order_item.is_item_cancelled:
                return serializers.ValidationError('This order item has already been cancelled!')
            if order.order_delivery_status in ["Shipped", "Delivered"]:
                return serializers.ValidationError(
                    "You can't cancel your order item after it has been shipped or delivered")
        except OrderItem.DoesNotExist:
            return serializers.ValidationError("No order item exists with given ID!")
        return attrs

    def create(self, validated_data):
        order_item_id = self.context['order_item_id']
        order_item = get_object_or_404(OrderItem, id=order_item_id)
        order_item.is_item_cancelled = True
        order_item.save()

        logger.info(f"Order Item with {order_item_id} cancelled successfully")
        return OrderItemCancellation.objects.create(order_item_id=order_item_id, **validated_data)
