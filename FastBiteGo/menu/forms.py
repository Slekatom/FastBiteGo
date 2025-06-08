from django import forms
from .models import *


class MenuFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      required=False,
                                      label="Оберіть Категорію")

class Search(forms.Form):
    title = forms.CharField(max_length=30)

class Review(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["title", "rating"]