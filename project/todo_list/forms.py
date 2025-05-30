from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'gls-input', 'placeholder': 'Username'
    }), label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'gls-input', 'placeholder': 'Password'
    }), label='Password')

class SignUpForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'gls-input','placeholder': 'First Name'
        }),label='FirstName', max_length=50)

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'gls-input','placeholder': 'Last Name'
        }),label='LastName', max_length=50)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'gls-input','placeholder': 'Username'
        }),label='Username', max_length=100)
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'gls-input', 'placeholder': 'Email'
    }),label='Email', max_length=100)
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'gls-input','placeholder': 'Password'
    }), label='Password1')

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'gls-input','placeholder': 'Confirm Password'
    }), label='Password2')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
    
