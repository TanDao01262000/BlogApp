from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Post, CustomUser
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
