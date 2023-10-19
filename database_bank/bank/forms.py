
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Credit

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class CreditRequestForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['amount', 'interest_rate', 'term']

