from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import *
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .models import *

class OrderCreateView(CreateView):
    model = Order
    template_name = "cart/order_create.html"
    form_class = OrderCreate

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = form.save()

        cart, created = Cart.objects.get_or_create(status="In progress", user=self.request.user)

        CartItems.objects.create(
            cart=cart,
            meal=order.meal,
            amount=order.amount,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("menu:landing")

