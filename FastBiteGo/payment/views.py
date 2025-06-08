from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import *
from .forms import *
from cart.models import Cart

class PaymentCreate(CreateView):
    model = Payment
    template_name = "payment/payment_create.html"
    form_class = PaymentCreate

    def form_valid(self, form):
        form.instance.user = self.request.user
        cart = Cart.objects.filter(status="In progress", user=self.request.user).first()
        form.instance.cart = cart
        form.save()
        cart.status = "History"
        cart.save()
        payment = form.instance
        if payment.choices == "Card":
            payment.purchase = "Purchased"
            payment.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cart:cart")