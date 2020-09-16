from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Post
from django import forms
from django.forms import ModelForm, Textarea


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'text-input',
               'label': 'Your Email Address'}
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text-input',
               'label': 'Create Password'}
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text-input',
               'label': 'Re-enter Password'}
    ))

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'login-input'}
    ))

    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'login-input'}
    ))

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'user']
        widgets = {
            'content': Textarea(attrs={'cols': 30, 'rows': 3})
        }
