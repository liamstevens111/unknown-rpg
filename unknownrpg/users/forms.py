from socket import fromshare
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import BaseUser

class UserSignUpForm(UserCreationForm):
    character_name = forms.CharField(max_length=20)

    class Meta:
        model = BaseUser
        fields = ('email', 'character_name', 'password1', 'password2')


class UserEditForm(UserChangeForm):
    class Meta:
        model = BaseUser
        fields = ('email', 'password',
                  'is_active', 'is_admin')