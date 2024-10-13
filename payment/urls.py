from django.urls import path
from .views import ProcessPaymentView, UserPaymentListView

urlpatterns = [
    path('process/', ProcessPaymentView.as_view(), name='process-payment'),
    path('list/', UserPaymentListView.as_view(), name='user-payments'),
]