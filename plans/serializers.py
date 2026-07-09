from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "duration_days", "property_limit"]


from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    plan_name = serializers.CharField(source="plan.name", read_only=True)
    property_limit = serializers.IntegerField(
        source="plan.property_limit", read_only=True
    )
    remaining_limit = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "property_used",
            "property_limit",
            "remaining_limit",
            "is_active",
        ]

    def get_remaining_limit(self, obj):
        return obj.remaining_limit()
