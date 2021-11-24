from django import forms
from django.contrib.auth.models import User
from . import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter the Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Reenter the password'}))

    class Meta():
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.userProfile
        # exclude = ['user',]
        exclude = ['user',]



class Answer(forms.ModelForm):
    answer = forms.CharField()

    class Meta():
        model = models.Answer
        fields = ('answer',)
