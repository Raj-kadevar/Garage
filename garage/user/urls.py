from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import UserLoginView, RegistrationView

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),

    path("email-verification/<int:id>",RegistrationView.as_view(),name="email_verification"),
]
