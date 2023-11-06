from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin

from user.models import Bike, Car, Garage, GarageWeekDay, CloseDay, Slot

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username", "email"]


@admin.register(Bike)
class Vehicle(admin.ModelAdmin):
    list_display = ["name", "owner", "image", "color", "mileage"]


@admin.register(Car)
class Vehicle(admin.ModelAdmin):
    list_display = ["name", "owner", "image", "color", "mileage"]


@admin.register(Garage)
class Garage(admin.ModelAdmin):
    list_display = ["name", "owner", "type"]


@admin.register(GarageWeekDay)
class Week(admin.ModelAdmin):
    list_display = ['choice', 'start_time', 'end_time', 'date', 'duration']

@admin.register(CloseDay)
class Day(admin.ModelAdmin):
    list_display = (['close_day', 'garage'])


@admin.register(Slot)
class Day(admin.ModelAdmin):
    list_display = (['start_time', 'end_time', 'GarageWeekDay'])