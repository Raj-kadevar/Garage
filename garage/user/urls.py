from django.contrib.auth.views import LogoutView
from django.urls import path, include

from user.views import UserLoginView, RegistrationView, VerficationView, HomeView

urlpatterns = [
    path("index/", HomeView.as_view(), name="index"),

    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),

    path("email-verification/<id>",VerficationView.as_view(),name="email_verification"),
]
