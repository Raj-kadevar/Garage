from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin

from user.models import Bike, Car

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