from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here.

# Index View
def index(request):
    return render(request, 'todo_list/index.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password.')
        else:
            form = LoginForm()
        return render(request, 'todo_list/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'todo_list/login.html', {'form': form})

# Sign Up View
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            user = User.objects.create_user(username, email, password1)
            
            return render(request, 'todo_list/sign_up_success.html')
        else:
            return render(request, 'todo_list/sign_up.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'todo_list/sign_up.html', {'form': form})