from django import forms
from .models import *


class PaymentCreate(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["choices"]