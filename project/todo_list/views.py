from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
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
        
    def check_username(request):
        username = request.POST.get('username')
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("<div id='username-error' class='gls-text-danger'>This username is already taken</div>")
        else:
            return HttpResponse("<div id='username-error' class='gls-text-success'>This username is available</div>")
        
    def check_email(request):
        email = request.POST.get('email')
        if get_user_model().objects.filter(email=email).exists():
            return HttpResponse("<div id='email-error' class='gls-text-danger'>This email is already linked to an account</div>")
        else:
            return HttpResponse("<div id='email-error' class='gls-text-success'>This email is available")

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
        form = CreateTaskForm()
        tasks = request.user.tasks.all()
        # checklist_items = Checklist_Item.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'todo_list/lists.html', {'tasks': tasks, 'form': form})
        
    class TaskList(ListView):
        template_name = 'lists.html'
        model = Checklist_Item
        context_object_name = 'tasks'

        def get_queryset(self):
            user = self.request.user
            return user.tasks.all()
        
    def add_task(request):
        task = request.POST.get('task')
        description = request.POST.get('description')

        new_task = Checklist_Item.objects.create(
            task=task,
            description=description,
            created_at = datetime.now(),
            is_complete = False)

        # add the task to the user's list
        request.user.tasks.add(new_task)

        # return template with all of the user's films
        tasks = request.user.tasks.all()
        form = CreateTaskForm()
        return render(request, 'todo_list/task_list.html', {'tasks': tasks, 'form': form})

        
    def put(self, request):
        form = EditTaskForm(request.PUT)

    class TaskDelete(DeleteView):
        model = Checklist_Item
        template_name = 'task_list.html'
    


class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/dashboard.html'