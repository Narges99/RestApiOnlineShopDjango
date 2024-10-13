from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, UpdateOrderSerializer, ListOrderSerializer, CreateOrderSerializer


class CreateOrderView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
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
        return Order.objects.filter(user=self.request.user)
