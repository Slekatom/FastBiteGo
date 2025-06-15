from django.shortcuts import render
from django.views.generic import ListView
from .models import *

class RequestList(ListView):
    model = Request
    template_name = "courier/requests.html"
    context_object_name = "requests"
