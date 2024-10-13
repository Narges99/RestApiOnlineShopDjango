from django.utils.datetime_safe import datetime
from rest_framework import serializers
from .models import Order
from cart.models import Cart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'status', 'total_amount', 'created_at']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'status']


class ListOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'id', 'order_number', 'status', 'total_amount', 'created_at']


class CreateOrderSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            cart = Cart.objects.filter(user=user, status='pending').first()
            if not cart or cart.lines.count() == 0:
                raise serializers.ValidationError("Cart is empty or not found.")
        except Cart.DoesNotExist:
            raise serializers.ValidationError("No cart found for this user.")

        order_number = f"ORD-{cart.id}-{datetime.now().strftime('%d-%m')}"
        order = Order.objects.create(
            user=user,
            order_number=order_number,
            cart=cart,
            status='pending',
            total_amount=0
        )

        order.total_amount = order.calculate_total()
        order.save()

        cart.status = 'closed'
        cart.save()

        return order
