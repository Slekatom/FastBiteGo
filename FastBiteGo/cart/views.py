from .forms import *
from django.views.generic import CreateView, FormView, DetailView, TemplateView, UpdateView, DeleteView, ListView
from django.urls import reverse, reverse_lazy
from .models import *
from django.shortcuts import get_object_or_404, redirect
from menu.models import Meal
from django.forms import modelformset_factory
from django.shortcuts import render


class OrderCreateView(CreateView):
    model = Order
    template_name = "cart/order_create.html"
    form_class = OrderCreate

    def form_valid(self, form):
        form.instance.user = self.request.user
        order = form.save()

        cart, created = Cart.objects.get_or_create(status="In progress", user=self.request.user)

        meal = order.meal
        if meal.stock < 1:
            form.add_error(None, "Немає достатньо товару в наявності.")
            return self.form_invalid(form)
        else:
            cartitem = CartItems.objects.create(
                cart=cart,
                meal=order.meal,
            )
            meal.stock -= cartitem.amount
            meal.save()
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

        cart, created = Cart.objects.get_or_create(user = self.request.user, status = "In progress")

        CartItems.objects.create(
            cart=cart,
            meal=order.meal
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cart:cart")

def remove_order(request, item_id):
    if request.method == "POST":
        order = get_object_or_404(CartItems, id=item_id)
        order.delete()
        order.meal.stock += order.amount
        order.meal.save()
    return redirect("cart:cart")

CartItemFormSet = modelformset_factory(
    CartItems,
    form=CartItemForm,
    extra=0
)

class CartView(ListView):
    model = CartItems
    template_name = "cart/cart.html"
    context_object_name = "items"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status="In progress")
        return cart.items.select_related('meal').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']

        total_amount = sum(item.meal.price * item.amount for item in items)

        CartItemFormSet = modelformset_factory(CartItems, form=CartItemForm, extra=0)
        formset = CartItemFormSet(queryset=items)

        context.update({
            'cart': items.first().cart if items.exists() else None,
            'total_amount': total_amount,
            'formset': formset,
        })
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user, status="In progress").first()
        items = CartItems.objects.filter(cart=cart)

        CartItemFormSet = modelformset_factory(CartItems, form=CartItemForm, extra=0)
        formset = CartItemFormSet(request.POST, queryset=items)

        total_amount = 0

        if formset.is_valid():
            for form in formset:
                print(f"Received amount: {form.cleaned_data.get('amount')}")
                item = form.save(commit=False)
                original = CartItems.objects.get(pk=item.pk)
                item.meal = original.meal
                item.cart = original.cart

                if item.amount > item.meal.stock:
                    form.add_error('amount', 'Немає стільки на складі')
                else:
                    item.total_price = item.amount * item.meal.price
                    item.save()

            if not formset.non_form_errors() and all(not f.errors for f in formset):
                return redirect('cart:cart')
        else:
            print(formset.errors)
            print(formset.non_form_errors())
            for form in formset:
                print(form.errors)
            total_amount = sum(item.meal.price * item.amount for item in items)

        return render(request, self.template_name, {
            'formset': formset,
            'cart': cart,
            'total_amount': total_amount,
        })



