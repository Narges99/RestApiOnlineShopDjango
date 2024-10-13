from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Cart
from .serializers import CartSerializer, AddToCartSerializer, RemoveFromCartSerializer


class CartListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class AddToCartView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"detail": "Product added to cart."}, status=status.HTTP_201_CREATED)


class RemoveFromCartView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.remove_product()
        return Response({"detail": "Product removed from cart and stock updated."}, status=status.HTTP_204_NO_CONTENT)
