from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(template_name='users/index.html'), name="logout"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
]