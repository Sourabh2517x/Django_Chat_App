from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "users/index.html"


class RegisterView(FormView):
    template_name = "users/auth_form.html"
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Register"
        return context


class CustomLoginView(LoginView):
    template_name = "users/auth_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"type":"Login"}
        )
        return context
