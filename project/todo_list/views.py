from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import *
from django.views.generic import *
from django.views import *


# Create your views here.

# Index View
def index(request):
    return render(request, 'todo_list/index.html')

# Sign Up View
class signup_view(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'todo_list/sign_up.html', {'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']

            user = User.objects.create_user(username, email, password1)
            
            return render(request, 'todo_list/sign_up_success.html')
        else:
            return render(request, 'todo_list/sign_up.html', {'form': form})

# Login View
class login_view(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'todo_list/login.html', {'form': form})
    
    def post(self, request):
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
    
class logout_view(LoginRequiredMixin, View):
    login_url = 'todo_list/login.html'

    def get(self, request):
        logout(request)
        return render(request, 'todo_list/index.html')
    
class list_view(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/lists.html'