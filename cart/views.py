from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Cart, CartLine
from .serializers import CartSerializer, AddToCartSerializer,  RemoveFromCartSerializer
from products.models import Product


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

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        if product.stock >= quantity:
            cart = Cart.objects.filter(user=request.user, status='pending').first()

            if not cart:
                cart = Cart.objects.create(user=request.user, status='pending')

            cart_line, created = CartLine.objects.get_or_create(cart=cart, product=product,
                                                                defaults={'quantity': quantity})
            if not created:
                cart_line.quantity += quantity
                cart_line.save()

            product.stock -= quantity
            product.save()
            return Response({"detail": "Product added to cart."}, status=status.HTTP_201_CREATED)
        else :
            return Response({"detail": "Requested quantity exceeds available stock."}, status=status.HTTP_400_BAD_REQUEST)



class RemoveFromCartView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RemoveFromCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            cart_id = serializer.validated_data['cart_id']

            try:
                cart = Cart.objects.get(user=request.user , id=cart_id  , status='pending')
                cart_line = CartLine.objects.get(cart=cart, product_id=product_id)
                product = Product.objects.get(id=product_id)
            except Cart.DoesNotExist:
                return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
            except CartLine.DoesNotExist:
                return Response({"detail": "Product not in cart."}, status=status.HTTP_404_NOT_FOUND)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

            product.stock += cart_line.quantity
            product.save()


            cart_line.delete()

            return Response({"detail": "Product removed from cart and stock updated."},
                            status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ClearCartView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         try:
#             cart = Cart.objects.get(user=request.user)
#             x= cart.created_at
#             cart.delete()
#             cart.created_at = None
#             x = cart.created_at
#             cart.save()
#
#             return Response({"detail": "Cart deleted successfully."}, status=status.HTTP_200_OK)
#
#         except Cart.DoesNotExist:
#             return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)