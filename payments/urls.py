from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, PaymentHistoryView

urlpatterns = [
    path("create-order/<int:plan_id>/", CreateOrderView.as_view(), name="create-order"),
    path("verify/", VerifyPaymentView.as_view(), name="verify-payment"),
    path("history/", PaymentHistoryView.as_view(), name="payment-history")
]
