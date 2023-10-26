from django.contrib.auth.models import AbstractUser
from django.db import models

from user.choices import COLOR_CHOICES


class User(AbstractUser):
    email = models.EmailField(unique=True,null=False,blank=False)


class CommonFields(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(choices=COLOR_CHOICES,null=False,blank=False)
    image = models.ImageField(upload_to="vehicles/")
    price = models.PositiveBigIntegerField(null=False,blank=False)
    plate_number = models.CharField(max_length=12,null=False,blank=False)
    mileage = models.PositiveSmallIntegerField(blank=False,null=False)
    class Meta:
        abstract = True

class Bike(CommonFields):
    pass

class Car(CommonFields):
    pass


