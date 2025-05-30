from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView
from django.urls import reverse, reverse_lazy


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("menu:landing")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

class RegisterView(CreateView):
    model = CustomUser
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse_lazy("menu:landing")

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

