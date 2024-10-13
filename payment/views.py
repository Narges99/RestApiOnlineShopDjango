from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer, PaymentProccessSerializer

class ProcessPaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentProccessSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        return Response({
            "detail": "Payment processed successfully.",
            "tracking_number": payment.tracking_number,
            "total_amount": payment.order.total_amount
        }, status=status.HTTP_201_CREATED)

class UserPaymentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(order__cart__user=self.request.user)
