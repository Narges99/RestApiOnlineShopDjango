from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer, PaymentProccessSerializer
import uuid

class ProcessPaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentProccessSerializer

    def create(self, request, *args, **kwargs):
        order_number = request.data.get('order_number')
        try:
            order = Order.objects.get(order_number=order_number, cart__user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == 'paid':
            return Response({"detail": "Order is already paid."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'paid'
        order.save()
        tracking_number = str(uuid.uuid4())

        payment = Payment.objects.create(
            order=order,
            tracking_number=tracking_number,
            status='completed'
        )

        return Response({
            "detail": "Payment processed successfully.",
            "tracking_number": tracking_number,
            "total_amount": order.total_amount
        }, status=status.HTTP_201_CREATED)

class UserPaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(order__cart__user=self.request.user)