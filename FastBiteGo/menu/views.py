from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, RedirectView
from .models import *

class MenuList(ListView):
    model = Category
    template_name = "menu/menu_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

class CategoryDetailView(DetailView):
    model = Category
    template_name = "menu/meal_list.html"
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        category = self.get_object()
        context = super().get_context_data(**kwargs)
        context["category"] = category
        return context
