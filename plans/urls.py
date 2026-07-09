from django.urls import path
from .views import PlanListView, ChoosePlanView, MySubscriptionView

urlpatterns = [
    path("", PlanListView.as_view(), name="plans"),
    path("choose/<int:plan_id>/", ChoosePlanView.as_view(), name="choose-plan"),
    path("my-subscription/", MySubscriptionView.as_view(), name="my-subscription"),
]
