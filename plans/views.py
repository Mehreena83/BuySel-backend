from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer


class ChoosePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        plan = get_object_or_404(Plan, id=plan_id)

        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=plan.duration_days)

        subscription, created = Subscription.objects.update_or_create(
            user=request.user,
            defaults={
                "plan": plan,
                "start_date": start_date,
                "end_date": end_date,
                "property_used": 0,
                "is_active": True,
            },
        )

        serializer = SubscriptionSerializer(subscription)

        return Response(
            {
                "message": "Plan activated successfully",
                "subscription": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(
            user=request.user, is_active=True
        ).first()

        if not subscription:
            return Response(
                {
                    "current_plan": "No Active Plan",
                    "property_used": 0,
                    "property_limit": 0,
                    "remaining_limit": 0,
                }
            )

        today = timezone.now().date()

        if subscription.end_date < today:
            subscription.is_active = False
            subscription.save()

            return Response(
                {
                    "current_plan": "No Active Plan",
                    "property_used": subscription.property_used,
                    "property_limit": subscription.plan.property_limit,
                    "remaining_limit": 0,
                    "is_active": False,
                    "message": "Your plan has expired. Please choose a new plan.",
                }
            )

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)
