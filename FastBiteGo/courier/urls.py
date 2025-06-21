from django.urls import path
from .views import *

app_name = "courier"

urlpatterns = [
    path("requests/", RequestList.as_view(), name = "requests"),
    path("requests/<int:request_pk>/take/", RequestUpdate.as_view(), name = "update"),
    path("requests/<int:pk>/", RequestDetailView.as_view(), name = "detail")
]