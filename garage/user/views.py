from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView
from rest_framework.reverse import reverse_lazy

from user.forms import Registration
from user.utils import send_email

User = get_user_model()
class  UserLoginView(LoginView):
    template_name = "login.html"


    def form_valid(self, form):
        super().form_valid(form)
        messages.success(self.request, 'login successful')
        return JsonResponse({'success': 'login successful'})

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse({'error': 'username or password invalid'})

class RegistrationView(CreateView):
    form_class = Registration
    template_name = "registration.html"

    def post(self, request, *args, **kwargs):
        user = Registration(request.POST)
        if user.is_valid():
            user = user.save()
            send_email(request, user)
            user.is_active = False
            user.save()
            messages.success(request, 'registration successful pls verify your email.')
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse(user.errors)

class VerficationView(View):
    def get(self, request, id, *args, **kwargs):
        user = User.objects.get(id = urlsafe_base64_decode(id).decode())
        user.is_active = True
        user.save()
        messages.success(request, f'{user.username} you are verified.')
        return redirect("login")

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class ResetPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "reset_password.html"
    success_url = reverse_lazy("login")



