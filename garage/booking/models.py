from django.db import models

from user.models import Garage, Slot, User


# Create your models here.

class Booking(models.Model):
    garage = models.ForeignKey(Garage,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)