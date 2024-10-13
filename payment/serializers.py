from rest_framework import serializers
from .models import Payment
from orders.models import Order
import uuid


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'tracking_number', 'status', 'payment_date']
        read_only_fields = ['status', 'payment_date']


class PaymentProccessSerializer(serializers.Serializer):
    order_number = serializers.CharField()

    def validate(self, data):
        order_number = data.get('order_number')
        try:
            order = Order.objects.get(order_number=order_number, cart__user=self.context['request'].user)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Order not found.")

        if order.status == 'paid':
            raise serializers.ValidationError("Order is already paid.")

        data['order'] = order
        return data

    def create(self, validated_data):
        order = validated_data['order']
        order.status = 'paid'
        order.save()

        tracking_number = str(uuid.uuid4())

        payment = Payment.objects.create(
            order=order,
            tracking_number=tracking_number,
            status='completed'
        )

        return payment
