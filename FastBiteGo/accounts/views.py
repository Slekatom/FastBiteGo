from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView, DetailView, TemplateView
from django.urls import reverse, reverse_lazy


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("menu:landing")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("menu:landing"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class RegisterView(CreateView):
    model = CustomUser
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("menu:landing"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("menu:landing")

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

class Profile(DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "profile"

class MyProfile(TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.request.user
        return context
