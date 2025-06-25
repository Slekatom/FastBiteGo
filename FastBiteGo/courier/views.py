from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, UpdateView, DetailView, CreateView
from django.http import HttpResponseBadRequest

from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin


class RequestList(LoginRequiredMixin, ListView):
    model = Request
    template_name = "courier/requests.html"
    context_object_name = "requests"
    redirect_field_name = 'next'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["requests2"] = Request.objects.filter(status="Queue")
        return context

class MyRequestList(LoginRequiredMixin, ListView):
    model = Request
    template_name = "courier/myrequests.html"
    context_object_name = "requests"
    redirect_field_name = 'next'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["my_requests"] = Request.objects.filter(courier = self.request.user, status = "Is Taken")
        context["user_request"] = Request.objects.filter(user = self.request.user, status = "Is Taken")
        context["usernow"] = self.request.user
        return context


class RequestUpdate(LoginRequiredMixin, UpdateView):
    model = Request
    template_name = "courier/take_request.html"
    success_url = reverse_lazy("courier:requests")
    fields = []
    context_object_name = "request"
    pk_url_kwarg = "request_pk"
    redirect_field_name = 'next'

    def form_valid(self, form):
        form.instance.status = "Is Taken"
        form.instance.courier = self.request.user
        if form.instance.courier != form.instance.user:
            form.save()
            request = form.instance
            chat = Chat.objects.create(user = request.user,
                                courier = self.request.user,
                                request = request)
            url = reverse('courier:detail', args=[chat.request.id])
            Message.objects.create(user = chat.courier,
                                   text = f"Кур'єр {chat.courier} прийняв замовлення {chat.user}. Переглянути замовлення: {url}",
                                   chat = chat)
            return super().form_valid(form)
        else:
            return HttpResponseBadRequest("Не дури систему, хай інший тобі доставить їжу!")


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = "courier/detail.html"
    context_object_name = "request_obj"
    pk_url_kwarg = "request_pk"
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_ob"] = self.get_object()
        return context

class MessageCreate(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "courier/chat.html"
    form_class = MessageForm
    redirect_field_name = 'next'

    def form_valid(self, form):
        chat_id = self.kwargs.get("chat_pk")
        chat = Chat.objects.get(id=chat_id)
        form.instance.chat = chat
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Форма невалидна:", form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("courier:chat", kwargs = {"chat_pk": self.kwargs["chat_pk"]})

    def get_context_data(self, **kwargs):
        chat_id = self.kwargs.get("chat_pk")
        chat = Chat.objects.get(id=chat_id)
        context = super().get_context_data(**kwargs)
        context["messages"] = Message.objects.filter(chat = chat)
        context["user_now"] = self.request.user
        return context