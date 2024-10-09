from django.urls import path
from .views import  AddToCartView, RemoveFromCartView, CartListView

urlpatterns = [
    path('cart/', CartListView.as_view(), name='cart-detail'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
