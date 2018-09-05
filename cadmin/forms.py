from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4,
                               max_length=200)
    email = forms.EmailField(label='Enter Email')
    password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        result = User.objects.filter(username=username)
        if result.count():
            raise ValidationError('Username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        result = User.objects.filter(email=email)
        if result.count():
            raise ValidationError('Email already exists')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match')
        return password2
    
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user
