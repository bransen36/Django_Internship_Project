from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, TaskForm
from django.contrib.auth import *
from django.contrib.auth.views import *
from django.contrib.auth.mixins import *
from django.views.generic import *
from django.views import *
from django.contrib import messages
from datetime import datetime
from todo_list.models import *


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
        return super().dispatch(request, *args, **kwargs)
    
class list_view(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/lists.html'

    def get(self, request):
        form = TaskForm()
        checklist_items = Checklist_Item.objects.filter(user=request.user).order_by('-created_at')
        return render(request, self.template_name, {
                'form': form,
                'checklist_items': checklist_items,
                'checklist_item_created': False
            })

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form_task = form.cleaned_data['task']
            form_description = form.cleaned_data['description']
            current_user = request.user
            current_time = datetime.now()
            complete = False

            checklistItem = Checklist_Item.objects.create(
                user = current_user,
                task = form_task,
                description = form_description,
                created_at = current_time,
                is_complete = complete
            )
            form = TaskForm()
            checklist_items = Checklist_Item.objects.filter(user=request.user).order_by('-created_at')
            return render(request, self.template_name, {
                'form': form,
                'checklist_items': checklist_items,
                'checklist_item_created': True
            })
        else:
            messages.error(request, "The given information was insufficient")
            checklist_items = Checklist_Item.objects.filter(user=request.user).order_by('-created_at')
            return render(request, self.template_name, {
                'form': form,
                'checklist_items': checklist_items,
                'checklist_item_created': False
            })
    


class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/dashboard.html'