from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("order/", OrderCreateView.as_view(), name = "order"),
    path("order/<int:pk>", OrderByIdCreateView.as_view(), name = "order_by_id"),
    path("", CartView.as_view(), name = "cart"),
    path("history/", HistoryView.as_view(), name = "history"),
    path("reorder/<int:cart_id>", reorder, name = "reorder"),
]