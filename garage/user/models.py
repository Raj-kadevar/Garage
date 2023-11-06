import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.choices import COLOR_CHOICES, DAY_CHOICES, VEHICLE_CHOICES


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


class GarageWeekDay(models.Model):
    choice = models.CharField(choices=DAY_CHOICES,null=False,blank=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    duration = models.TimeField(default=datetime.timedelta(minutes=60))
    def __str__(self):
        return self.choice


class Garage(models.Model):
    name = models.CharField(max_length=20, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    workingday = models.ManyToManyField(GarageWeekDay)
    type = models.CharField(choices=VEHICLE_CHOICES,default='ALL')

    def __str__(self):
        return self.name


class CloseDay(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    close_day = models.CharField(choices=DAY_CHOICES)



class Slot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    GarageWeekDay = models.ForeignKey(GarageWeekDay, on_delete=models.CASCADE)

