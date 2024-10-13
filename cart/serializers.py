from rest_framework import serializers
from .models import Cart, CartLine
from products.serializers import ProductSerializer
from products.models import Product


class CartLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartLine
        fields = ['product', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    lines = CartLineSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'lines', 'status']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate(self, data):
        product_id = data.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        if product.stock < data['quantity']:
            raise serializers.ValidationError("Requested quantity exceeds available stock.")

        return data

    def save(self, user):
        product = Product.objects.get(id=self.validated_data['product_id'])
        quantity = self.validated_data['quantity']

        cart, created = Cart.objects.get_or_create(user=user, status='pending')
        cart_line, created = CartLine.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})

        if not created:
            cart_line.quantity += quantity
            cart_line.save()

        product.stock -= quantity
        product.save()

        return cart


class RemoveFromCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    cart_id = serializers.IntegerField(required=True)

    def validate(self, data):
        try:
            Cart.objects.get(id=data['cart_id'], user=self.context['request'].user, status='pending')
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart not found or not in pending state.")

        try:
            Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

        return data

    def remove_product(self):
        cart = Cart.objects.get(id=self.validated_data['cart_id'], user=self.context['request'].user, status='pending')
        cart_line = CartLine.objects.get(cart=cart, product_id=self.validated_data['product_id'])

        product = Product.objects.get(id=self.validated_data['product_id'])
        product.stock += cart_line.quantity
        product.save()

        cart_line.delete()
