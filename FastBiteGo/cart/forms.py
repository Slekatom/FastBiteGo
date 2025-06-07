from django import forms
from .models import Order, CartItems

class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["meal"]

class OrderByIdCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItems
        fields = ["amount"]
