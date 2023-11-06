from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from booking.models import Booking
from user.models import Slot, Garage


# Create your views here.

class BookSlot(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        print(request.POST['slot'])
        slot = Slot.objects.get(id=request.POST['slot'])
        garage = Garage.objects.filter(workingday=slot.GarageWeekDay).first()
        Booking.objects.create(slot=slot,user=request.user,garage=garage)
        return JsonResponse({'success': 'successful'})
