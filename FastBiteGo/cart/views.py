from django.shortcuts import get_list_or_404
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
            cartitem_search = CartItems.objects.filter(cart=cart, meal=meal)
            if not cartitem_search.exists():
                CartItems.objects.create(
                    cart=cart,
                    meal=meal,
                )
            else:
                form.add_error(None, "Товар вже у кошику.")
                return self.form_invalid(form)


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

        if meal.stock < 1:
            form.add_error(None, "Немає достатньо товару в наявності.")
            return self.form_invalid(form)
        else:
            cartitem_search = CartItems.objects.filter(cart=cart, meal=meal)
            if not cartitem_search.exists():
                CartItems.objects.create(
                    cart=cart,
                    meal=meal,
                )
            else:
                form.add_error(None, "Товар вже у кошику.")
                return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cart:cart")

# def remove_order(request, item_id):
#     if request.method == "POST":
#         order = get_object_or_404(CartItems, id=item_id)
#         order.delete()
#         order.meal.stock += order.amount
#         order.meal.save()
#     return redirect("cart:cart")

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
            'total_amount': total_amount,
            'formset': formset,
        })
        return context

    def post(self, request):
        cart = Cart.objects.filter(user=request.user, status="In progress").first()
        cart_items = CartItems.objects.filter(cart=cart)

        CartItemFormSet = modelformset_factory(CartItems, form=CartItemForm, extra=0)
        formset = CartItemFormSet(request.POST, queryset=cart_items)

        if 'delete' in request.POST:
            # Кнопка удаления нажата
            item_id = request.POST.get('delete')
            item_to_delete = get_object_or_404(CartItems, id=item_id, cart=cart)
            item_to_delete.delete()
            item_to_delete.meal.progress_stock = item_to_delete.meal.stock
            item_to_delete.meal.save()
            return redirect('cart:cart')

        elif 'update' in request.POST:
            # Обновление количества
            total_amount = 0
            if formset.is_valid():
                for form in formset:
                    item = form.save(commit=False)
                    original = CartItems.objects.get(pk=item.pk)
                    item.meal = original.meal
                    item.cart = original.cart

                    if item.amount > item.meal.stock:
                        form.add_error('amount', 'Немає стільки на складі')
                    else:
                        item.total_price = item.amount * item.meal.price
                        item.save()
                        item.meal.progress_stock = item.meal.stock - item.amount
                        item.meal.save()
                        total_amount += item.total_price

                if not formset.non_form_errors() and all(not f.errors for f in formset):
                    return redirect('cart:cart')

            return render(request, self.template_name, {
                'formset': formset,
                'cart': cart,
                'total_amount': total_amount,
            })

        return redirect('cart:cart')

class HistoryView(ListView):
    model = CartItems
    template_name = "cart/history.html"
    context_object_name = "items"

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, status="In progress")
        return cart.items.select_related('meal').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history = get_list_or_404(Cart, user = self.request.user, status = "History")
        cartitems = get_list_or_404(CartItems)
        context["history"] = history
        context["cartitems"] = cartitems
        return context

def reorder(request, cart_id):
    cart = get_object_or_404(Cart, id = cart_id, status = "History")
    new_cart = get_object_or_404(Cart, status = "In progress", user = request.user)

    new_cart.items.all().delete()

    for item in cart.items.all():
        CartItems.objects.create(
            cart = new_cart,
            meal = item.meal,
            amount = item.amount
        )
    return redirect('cart:cart')







