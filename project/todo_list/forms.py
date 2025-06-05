from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')

class SignUpForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(),label='FirstName', max_length=50)
    last_name = forms.CharField(widget=forms.TextInput(),label='LastName', max_length=50)
    username = forms.CharField(widget=forms.TextInput(),label='Username', max_length=100)
    email = forms.EmailField(widget=forms.EmailInput(),label='Email', max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password1')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Password2')

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        
class CreateTaskForm(forms.Form):
    task = forms.CharField(widget=forms.TextInput(), label='task', max_length=100)
    description = forms.CharField(widget=forms.Textarea(), label='description', required=False)

class EditTaskForm(forms.Form):
    task = forms.CharField(widget=forms.TextInput(), label='task', max_length=100)
    description = forms.CharField(widget=forms.Textarea(), label='description', required=False)
    is_complete = forms.ChoiceField()

class DeleteTaskForm(forms.Form):
    pass
    
