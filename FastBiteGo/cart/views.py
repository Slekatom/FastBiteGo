from .forms import *
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy
from .models import *
from django.shortcuts import get_object_or_404, redirect
from menu.models import Meal

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
        return reverse_lazy("cart:cart")

class OrderByIdCreateView(CreateView):
    model = Order
    template_name = "cart/order_by_id_create.html"
    form_class = OrderByIdCreate

    def dispatch(self, request, *args, **kwargs):
        self.meal = get_object_or_404(Meal, pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        meal = self.meal
        form.instance.user = self.request.user
        form.instance.meal = meal
        order = form.save()

        cart, created = Cart.objects.get_or_create(user = self.request.user, status = "In Progress")

        CartItems.objects.create(
            cart=cart,
            meal=order.meal,
            amount=order.amount,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cart:cart")

def remove_order(request, item_id):
    if request.method == "POST":
        order = get_object_or_404(CartItems, id=item_id)
        order.delete()
    return redirect("cart:cart")

class CartView(ListView):
    model = CartItems
    template_name = "cart/cart.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, created = Cart.objects.get_or_create(user = self.request.user, status = "In Progress")
        context["cart"] = cart
        return context

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status="In Progress")
        return cart.items.all()


