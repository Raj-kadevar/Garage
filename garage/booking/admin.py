from django.contrib import admin

from booking.models import Booking


@admin.register(Booking)
class Book(admin.ModelAdmin):
    list_display = ["slot", "garage", 'user']