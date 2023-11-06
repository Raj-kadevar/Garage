import datetime
import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from user.forms import Registration, CarRegistration, BikeRegistration, CarUpdateForm, BikeUpdateForm, GarageForm, \
    GarageWeekDayForm, RepairVehicleForm
from user.models import Bike, Car, Garage, CloseDay, Slot, GarageWeekDay
from user.utils import send_email

User = get_user_model()
class  UserLoginView(LoginView):
    template_name = "login.html"


    def form_valid(self, form):
        super().form_valid(form)
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
        if group.name == 'Vehicle owner':
            cars = Car.objects.filter(owner = request.user)[0:2]
            bikes = Bike.objects.filter(owner = request.user)[0:2]
            return render(request, "index.html",{'bikes':bikes, 'cars':cars})
        else:
            garages = Garage.objects.all()
            return render(request, "admin/admin.html", {'garages': garages})


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


class AddGarage(LoginRequiredMixin, CreateView):
    form_class = GarageForm
    template_name = "garage_form.html"
    def post(self, request, *args, **kwargs):
        garage = GarageForm(request.POST)
        if garage.is_valid():
            garage = garage.save()
            bulk_list = []
            for x in request.POST.getlist('off_day'):
                close_day = CloseDay(garage=garage, close_day=x)
                bulk_list.append(close_day)
            CloseDay.objects.bulk_create(bulk_list)
            return redirect('index')
        else:
            errors = garage.errors
            return render(request, "garage_form.html", {"errors": errors, "form": garage})


class AddSchedule(LoginRequiredMixin, CreateView):
    form_class = GarageWeekDayForm
    template_name = "schedule_form.html"
    def post(self, request, *args, **kwargs):
        schedule = GarageWeekDayForm(request.POST)
        if schedule.is_valid():
            schedule = schedule.save()
            start_time = schedule.start_time
            end_time = schedule.end_time
            duration = schedule.duration
            slot = start_time
            duration = datetime.datetime.combine(datetime.datetime.today(), duration)
            start_time = datetime.datetime.combine(datetime.datetime.today(), start_time)

            end_time = datetime.datetime.combine(datetime.datetime.today(), end_time)

            slot = start_time
            start_time = slot
            while True:
                slot = slot + datetime.timedelta(hours=duration.hour, minutes=duration.minute)
                if slot < end_time:
                    Slot.objects.create(start_time=start_time, end_time=slot.time(), GarageWeekDay=schedule)
                    start_time = slot
                else:
                    break
            return redirect('index')
        else:
            errors = schedule.errors
            return render(request, "schedule_form.html", {"errors": errors, "form": schedule})


class UpdateGarage(LoginRequiredMixin, UpdateView):
    permission_required = ('user.change_category',)
    form_class = GarageForm
    template_name = "garage_form.html"
    success_url = reverse_lazy("index")
    queryset = Garage.objects.all()



class DeleteGarage(LoginRequiredMixin, DeleteView):
    model = Garage
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("index")


class RepairVehicle(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        html = render_to_string("repair_vehicle.html", {'form': RepairVehicleForm})
        return JsonResponse({'page': html})

    def post(self, request, *args, **kwargs):
        schedule = RepairVehicleForm(request.POST)
        if schedule.is_valid():
            week_day = GarageWeekDay.objects.get(date=request.POST['date'])
            slots = Slot.objects.filter(GarageWeekDay=week_day)
            if request.POST['type'] == 'ALL':
                garages = Garage.objects.filter(workingday=week_day)
            else:
                garages = Garage.objects.filter(workingday=week_day, type=request.POST['type'])
            html = render_to_string("slot_book.html", {'week_day': week_day,'slots':slots})
            return JsonResponse({'page': html})
        else:
            return JsonResponse(schedule.errors)

