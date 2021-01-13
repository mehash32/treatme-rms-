from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from Food.models import Profile
from django import forms
from .models import UserProfile

class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['is_manager']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'example@gmail.com'}),
        }
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        widgets = {
            'Phone_number': forms.TextInput(attrs={'placeholder': '+880xxxxxxxxxx'})
        }
        fields = ['Profile_picture', 'Phone_number']
