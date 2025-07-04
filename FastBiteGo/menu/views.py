from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView, RedirectView
from .models import *
from .forms import *
from django import forms

class MenuList(ListView):
    model = Category
    template_name = "menu/menu_list.html"
    context_object_name = "categories"
    filter_form = None
    search_form = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = MenuFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            selected_category = self.filter_form.cleaned_data.get("category")
            if selected_category:
                queryset = queryset.filter(id=selected_category.id)

        self.search_form = Search(self.request.GET or None)
        if self.search_form.is_valid():
            searched = self.search_form.cleaned_data.get("title")
            if searched:
                queryset = queryset.filter(
                    Q(title__icontains=searched) |
                    Q(meal__title__icontains=searched)
                ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = self.filter_form
        context["search"] = self.search_form
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

class MealDetailView(DetailView):
    model = Meal
    template_name = "menu/meal.html"
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        meal = self.get_object()
        reviews = Review.objects.filter(meal = meal)
        context = super().get_context_data(**kwargs)
        context["meal"] = meal
        context["reviews"] = reviews
        context["usernow"] = self.request.user
        return context

class ReviewCreateView(CreateView):
    model = Review
    template_name = "menu/meal_review.html"
    form_class = ReviewForm

    def form_valid(self, form):
        meal_pk = self.kwargs.get('meal_pk')
        form.instance.user = self.request.user
        form.instance.meal = get_object_or_404(Meal, id = meal_pk)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("menu:landing")

