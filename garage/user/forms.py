from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms

from user.models import Car, Bike

User = get_user_model()

class Registration(UserCreationForm):
    groups = [(name, name) for name in Group.objects.all().values_list('name', flat=True)]
    roles = forms.ChoiceField(choices=groups)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['id'] = 'form1Example23'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = User
        fields = ['email', 'username',  'password1', 'password2', 'roles']

class CarRegistration(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['id'] = visible.field.label
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = Car
        fields = ['name', 'price',  'plate_number', 'color', 'image', 'mileage']


class BikeRegistration(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['id'] = visible.field.label
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = Bike
        fields = ['name', 'price',  'plate_number', 'color', 'image', 'mileage']

