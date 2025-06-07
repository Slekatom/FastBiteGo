from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("order/", OrderCreateView.as_view(), name = "order"),
    path("order/<int:pk>", OrderByIdCreateView.as_view(), name = "order_by_id"),
    path("<int:item_id>/remove", remove_order, name = "remove"),
    path("", CartView.as_view(), name = "cart"),
]