from django.urls import path
from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", LoginView.as_view(), name = "login"),
    path("register/", RegisterView.as_view(), name = "register"),
    path("logout/", logout_view, name = "logout"),
    path("profile/<int:pk>", Profile.as_view(), name = "profile"),
    path("profile/my/", MyProfile.as_view(), name = "my_profile"),
]