from rest_framework import serializers
from .models import Payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    plan_duration = serializers.IntegerField(source="plan.duration_days", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "plan_name",
            "plan_duration",
            "amount",
            "status",
            "razorpay_order_id",
            "razorpay_payment_id",
            "created_at",
        ]