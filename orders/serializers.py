from rest_framework import serializers
from .models import Order

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
        fields = [  'user', 'id','order_number', 'status', 'total_amount', 'created_at']

