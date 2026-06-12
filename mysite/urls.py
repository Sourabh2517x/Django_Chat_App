from django.contrib import admin
from django.urls import path,include
from users import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("users/", include('users.urls')),
    path("chatbot/", include('chatbot.urls')),
    path("admin/", admin.site.urls),
]
