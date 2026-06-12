from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.ChatView.as_view(), name="chat"),
    path("plan/", views.PlanView.as_view(), name="plan"),
]