from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

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
        
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone_number', 'address1', 'address2']
    # first_name = forms.CharField(widget=forms.TextInput(), label='firstname')
    # last_name = forms.CharField(widget=forms.TextInput(), label='lastname')
    # username = forms.CharField(widget=forms.TextInput(), label='username')
    # phone_number = forms.IntegerField(widget=forms.TextInput(), label='phone', required=False)
    # address1 = forms.CharField(widget=forms.TextInput(), label='address1', required=False)
    # address2 = forms.CharField(widget=forms.TextInput(), label='address2', required=False)
        
class CreateTaskForm(forms.Form):
    task = forms.CharField(widget=forms.TextInput(), label='task', max_length=100)
    description = forms.CharField(widget=forms.Textarea(), label='description', required=False)

class EditTaskForm(forms.Form):
    task = forms.CharField(widget=forms.TextInput(), label='task', max_length=100)
    description = forms.CharField(widget=forms.Textarea(), label='description', required=False)
    is_complete = forms.TypedChoiceField(
    choices=[(True, 'Complete'), (False, 'Incomplete')],
    coerce=lambda x: x == 'True',
    widget=forms.RadioSelect(attrs={'class': 'gls-radio'}),
    label='Is Complete',
    empty_value=None
    )
    
