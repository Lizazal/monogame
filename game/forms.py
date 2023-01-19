from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from game.models import UsersInfo
from django.db import models
from django.contrib.auth.models import AbstractUser


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = UsersInfo
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'age', 'sex', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'class': 'form-input'}),
            'sex': forms.RadioSelect(attrs={'class': 'centered'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
