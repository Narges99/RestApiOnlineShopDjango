from rest_framework import serializers
from .models import Cart, CartLine
from products.serializers import ProductSerializer


class CartLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = CartLine
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    lines = CartLineSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id','user', 'created_at', 'lines' , 'status']

class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    cart_id = serializers.IntegerField(required=True)



class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


