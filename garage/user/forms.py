from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import forms

User = get_user_model()

class Registration(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.field.widget.attrs['id'] = 'form1Example23'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    class Meta:
        model = User
        fields = ['email', 'username',  'password1', 'password2']

