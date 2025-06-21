from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView
from .models import *

class RequestList(ListView):
    model = Request
    template_name = "courier/requests.html"
    context_object_name = "requests"

class RequestUpdate(UpdateView):
    model = Request
    template_name = "courier/take_request.html"
    success_url = reverse_lazy("courier:requests")
    fields = []
    context_object_name = "request"
    pk_url_kwarg = "request_pk"

    def form_valid(self, form):
        form.instance.status = "Is Taken"
        form.instance.courier = self.request.user
        form.save()
        request = self.get_object()
        Chat.objects.create(user = request.user,
                            courier = self.request.user,
                            request = request)
        return super().form_valid(form)

class RequestDetailView(DetailView):
    model = Request
    template_name = "courier/detail.html"
    context_object_name = "request_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_ob"] = self.get_object()
        return context

