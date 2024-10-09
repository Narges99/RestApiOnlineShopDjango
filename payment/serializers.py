from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'tracking_number', 'status', 'payment_date']
        read_only_fields = ['status', 'payment_date']


class PaymentProccessSerializer(serializers.Serializer):
    order_number = serializers.CharField()
