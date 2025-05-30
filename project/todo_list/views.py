from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import *
from django.contrib.auth.views import *
from django.contrib.auth.mixins import *
from django.views.generic import *
from django.views import *
from django.contrib import messages


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
            User = get_user_model()
            firstName = form.cleaned_data['first_name']
            lastName = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']


            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password1,
                    first_name = firstName,
                    last_name = lastName
                )
                
                login(request, user)
                return render(request, 'todo_list/dashboard.html')
            else:
                messages.error(request, "An account with this email already exists.")
                return render(request, 'todo_list/sign_up.html', {'form': form})
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
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
        else:
            form = LoginForm()
        return render(request, 'todo_list/login.html', {'form': form})
    
class logout_view(LoginRequiredMixin, LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You've been logged out.")
        return super().dispatch(request, *args, **kwargs)
    
class list_view(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/lists.html'

class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/dashboard.html'