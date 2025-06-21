from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "Is Taken"
        form.save()
        return super().form_valid(form)
