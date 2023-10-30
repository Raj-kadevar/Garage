import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from user.forms import Registration, CarRegistration, BikeRegistration, CarUpdateForm, BikeUpdateForm
from user.models import Bike, Car
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
            user.groups.add(Group.objects.get(name=request.POST['roles']))
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

class HomeView(LoginRequiredMixin, View):
    # template_name = "index.html"
    def get(self, request, *args, **kwargs):
        group = Group.objects.filter(user=request.user).first()
        if group.name == 'vehicle owner':
            cars = Car.objects.filter(owner = request.user)[0:2]
            bikes = Bike.objects.filter(owner = request.user)[0:2]
            return render(request, "index.html",{'bikes':bikes, 'cars':cars})
        else:
            return redirect("login")



class ResetPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = "reset_password.html"
    success_url = reverse_lazy("login")

class CarRegistrationView(CreateView):
    form_class = CarRegistration
    template_name = "car_form.html"

    def post(self, request, *args, **kwargs):
        car = CarRegistration(request.POST , request.FILES)
        if car.is_valid():
            car = car.save(commit=False)
            car.owner = request.user
            car.save()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse(car.errors)


class BikeRegistrationView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        bike = BikeRegistration(request.POST, request.FILES)
        if bike.is_valid():
            bike = bike.save(commit=False)
            bike.owner = request.user
            bike.save()
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse(bike.errors)


class BikeList(LoginRequiredMixin, View):
    def get(self, request):
        bikes = Bike.objects.filter(owner = request.user)
        html = render_to_string("bike_list.html",{'bikes':bikes})
        return JsonResponse({'page': html})

class CarList(LoginRequiredMixin, View):
    def get(self, request):
        cars = Car.objects.filter(owner = request.user)
        html = render_to_string("car_list.html",{'cars':cars})
        return JsonResponse({'page': html})


class CarUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Car.objects.filter(id = kwargs.get('pk'))
        serialized_data = serialize("json", form)
        form = json.loads(serialized_data)
        return JsonResponse(form, safe=False)

    def post(self, request, *args, **kwargs):
        car = CarUpdateForm(request.POST)
        if car.is_valid():
            car = Car.objects.get(id=kwargs.get('pk'))
            car.name = request.POST['name']
            car.price = request.POST['price']
            car.color = request.POST['color']
            car.plate_number = request.POST['plate_number']
            car.mileage = request.POST['mileage']
            car.save()
            return JsonResponse({'message': 'success'})
        else:
            print("INVALID___________")
            return JsonResponse(car.errors)

class BikeUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Bike.objects.filter(id = kwargs.get('pk'))
        serialized_data = serialize("json", form)
        form = json.loads(serialized_data)
        return JsonResponse(form, safe=False)

    def post(self, request, *args, **kwargs):
        bike = BikeUpdateForm(request.POST)
        if bike.is_valid():
            bike = Bike.objects.get(id=kwargs.get('pk'))
            bike.name = request.POST['name']
            bike.price = request.POST['price']
            bike.color = request.POST['color']
            bike.plate_number = request.POST['plate_number']
            bike.mileage = request.POST['mileage']
            bike.save()
            return JsonResponse({'message': 'successful'})
        else:
            return JsonResponse(bike.errors)

class BikeDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Bike.objects.get(id = kwargs.get('pk')).delete()
        return JsonResponse({'message': 'successful'})


class CarDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        Car.objects.get(id = kwargs.get('pk')).delete()
        return JsonResponse({'message': 'successful'})
