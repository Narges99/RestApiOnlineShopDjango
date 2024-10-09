from django.urls import path
from .views import CreateOrderView, UpdateOrderStatusView, ListUserOrdersView

urlpatterns = [
    path('orders/', ListUserOrdersView.as_view(), name='user-orders'),
    path('order/create/', CreateOrderView.as_view(), name='create-order'),
    path('order/update/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]
