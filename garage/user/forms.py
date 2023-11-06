import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory

from user.choices import DAY_CHOICES, VEHICLE_CHOICES
from user.models import Car, Bike, Garage, CloseDay, GarageWeekDay

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


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'price', 'plate_number', 'color', 'mileage']


class BikeUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'price', 'plate_number', 'color', 'mileage']


class GarageForm(forms.ModelForm):
    off_day = forms.MultipleChoiceField(choices=DAY_CHOICES)

    class Meta:
        model = Garage
        fields = ['name', 'owner', 'workingday', 'type', 'off_day']



class GarageWeekDayForm(forms.ModelForm):
    class Meta:
        model = GarageWeekDay
        fields = ['choice', 'start_time', 'end_time', 'date', 'duration']

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past")
        return date


class RepairVehicleForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    type = forms.ChoiceField(choices=VEHICLE_CHOICES)
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past")
        return date