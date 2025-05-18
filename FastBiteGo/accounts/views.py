from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse

class LoginView(CreateView):
    model = CustomUser
    template_name = "accounts/login.html"
    from_class = AuthenticationForm

    def get_success_url(self):
        return redirect(reverse('landing:'))

class RegisterView(CreateView):
    model = CustomUser
    template_name = "accounts/register.html"
    from_class = CustomUserCreationForm

    def get_success_url(self):
        return redirect(reverse("landing:"))

def logout_view(request):
    logout(request)
    return redirect('login')

