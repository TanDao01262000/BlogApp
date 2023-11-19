from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Post, CustomUser, Profile
from django import forms


class UserRegisterForm(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


# class for update profile
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    linkedin_link = forms.URLField(required=False)
    
    class Meta:
        model = Profile
        fields = ['bio', 'linkedin_link']