import razorpay
from datetime import timedelta
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from plans.models import Plan, Subscription
from .models import Payment
from rest_framework import generics
from .serializers import PaymentHistorySerializer

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        if request.user.role != "agent":
            return Response(
                {"error": "Only agents can choose a plan."},
                status=status.HTTP_403_FORBIDDEN,
            )

        plan = get_object_or_404(Plan, id=plan_id)

        amount_in_paise = int(plan.price * 100)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create(
            {
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1,
            }
        )

        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            razorpay_order_id=razorpay_order["id"],
            status="created",
        )

        return Response(
            {
                "message": "Order created successfully",
                "order_id": razorpay_order["id"],
                "amount": amount_in_paise,
                "currency": "INR",
                "key": settings.RAZORPAY_KEY_ID,
                "payment_id": payment.id,
                "plan": {
                    "id": plan.id,
                    "name": plan.name,
                    "price": plan.price,
                },
            },
            status=status.HTTP_201_CREATED,
        )

class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "agent":
            return Response(
                {"error": "Only agents can verify payment."},
                status=status.HTTP_403_FORBIDDEN,
            )

        payment_id = request.data.get("payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            user=request.user,
            razorpay_order_id=razorpay_order_id,
        )

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )

            payment_method = None

            try:
                payment_details = client.payment.fetch(razorpay_payment_id)
                payment_method = payment_details.get("method")
                print("RAZORPAY PAYMENT DETAILS:", payment_details)
                print("PAYMENT METHOD:", payment_method)
            except Exception as fetch_error:
                print("RAZORPAY PAYMENT FETCH ERROR:", fetch_error)

            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.payment_method = payment_method
            payment.status = "success"
            payment.save()

            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=payment.plan.duration_days)

            Subscription.objects.update_or_create(
                user=request.user,
                defaults={
                    "plan": payment.plan,
                    "start_date": start_date,
                    "end_date": end_date,
                    "property_used": 0,
                    "is_active": True,
                },
            )

            return Response(
                {
                    "message": "Payment verified and plan activated successfully",
                    "payment_method": payment.payment_method,
                }
            )

        except Exception as error:
            print("PAYMENT VERIFY ERROR:", error)

            payment.status = "failed"
            payment.save()

            return Response(
                {"error": "Payment verification failed", "details": str(error)},
                status=status.HTTP_400_BAD_REQUEST,
            )
class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-created_at")