from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    email = models.EmailField(unique=True,null=False,blank=False)
    verify = models.BooleanField(default=False)