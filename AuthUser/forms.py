from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=124, required=True)

    class Meta:
        model = User
        fields =['username', 'email', 'password1', 'password2']

class Login(forms.Form):
    login = forms.CharField(max_length=150)
    password = forms.CharField(max_length=150)