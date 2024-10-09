from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Order
from cart.models import Cart
from .serializers import OrderSerializer, UpdateOrderSerializer, ListOrderSerializer
from rest_framework.response import Response

class CreateOrderView(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.filter(user=request.user, status='pending').first()
        except Cart.DoesNotExist:
            return Response({"detail": "No cart found for this user."}, status=status.HTTP_404_NOT_FOUND)
        if cart.lines.count() == 0:
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)
        x = "ORD-" + str(cart.id)+'-' + datetime.now().strftime("%-d-%-m")
        order = Order.objects.create(
            user= request.user,
            order_number="ORD-" + str(cart.id)+'-' + datetime.now().strftime("%-d-%-m"),
            cart=cart,
            status='pending',
            total_amount=0
        )
        order.total_amount = order.calculate_total()
        order.save()
        cart.status = 'closed'
        cart.save()
        return Response({"detail": "Order created successfully.", "order_number": order.order_number}, status=status.HTTP_201_CREATED)


class UpdateOrderStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateOrderSerializer

    def get_object(self):
        order_number = self.request.data.get('order_number')
        return Order.objects.get(order_number=order_number, cart__user=self.request.user)

class ListUserOrdersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        t = self.request.user
        y = Order.objects.filter(user=self.request.user)
        u = Order.objects.all()
        return Order.objects.filter(user=self.request.user)