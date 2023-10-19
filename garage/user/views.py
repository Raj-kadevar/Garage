from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from user.forms import Registration
from user.utils import send_email


class  UserLoginView(LoginView):
    template_name = "login.html"


class RegistrationView(CreateView):
    form_class = Registration
    template_name = "registration.html"

    def post(self, request, *args, **kwargs):
        print("inside post")
        user = Registration(request.POST)
        if user.is_valid():
            user = user.save()
            # # try:
            # send_email(request, user)
            # # except Exception as e:
            # #     print(e)
            messages.success(request, 'registration successful pls verify your email.')
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse(user.errors)
