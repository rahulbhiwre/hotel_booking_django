from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ValidationError
from .models import User,Customer
from django.db import transaction



class HotelSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email', 
            'password1', 
            'password2', 
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_hotel = True
        if commit:
            user.save()
        return user


class CustomerSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email', 
            'password1', 
            'password2', 
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        return user