# from datetime import timedelta
# from rest_framework import serializers
# from .models import Payment

# #Paymemt history 
# class PaymentHistorySerializer(serializers.ModelSerializer):
#     plan_name = serializers.CharField(source="plan.name", read_only=True)
#     plan_duration = serializers.IntegerField(source="plan.duration_days", read_only=True)
#     plan_taken_date = serializers.SerializerMethodField()
#     expire_date = serializers.SerializerMethodField()

#     class Meta:
#         model = Payment
#         fields = [
#             "id",
#             "plan_name",
#             "plan_duration",
#             "amount",
#             "status",
#             "payment_method",
#             "plan_taken_date",
#             "expire_date",
#             "razorpay_order_id",
#             "razorpay_payment_id",
#             "created_at",
#         ]

#     def get_plan_taken_date(self, obj):
#         if not obj.created_at:
#             return None
#         return obj.created_at.date()

#     def get_expire_date(self, obj):
#         if obj.status != "success":
#             return None

#         if not obj.created_at or not obj.plan:
#             return None

#         return obj.created_at.date() + timedelta(days=obj.plan.duration_days)



from datetime import timedelta
from rest_framework import serializers
from .models import Payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    plan_duration = serializers.IntegerField(source="plan.duration_days", read_only=True)
    plan_taken_date = serializers.SerializerMethodField()
    expire_date = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "plan_name",
            "plan_duration",
            "amount",
            "status",
            "payment_method",
            "plan_taken_date",
            "expire_date",
            "razorpay_order_id",
            "razorpay_payment_id",
            "created_at",
        ]

    def get_plan_taken_date(self, obj):
        if not obj.created_at:
            return None

        return obj.created_at.date()

    def get_expire_date(self, obj):
        if not obj.created_at or not obj.plan:
            return None

        return obj.created_at.date() + timedelta(days=obj.plan.duration_days)