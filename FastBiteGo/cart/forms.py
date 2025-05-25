from django import forms
from .models import Order
class OrderCreate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["meal", "amount"]
