from django import forms

# from django.contrib.auth.models import User
from accounts.models import Register
from django.contrib.auth.forms import UserCreationForm


class Loginform(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter UserName', 'style': 'width: 300px; height:60px;margin-left:15px;'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'style': 'width: 300px;height:60px;margin-left:20px;'}))
