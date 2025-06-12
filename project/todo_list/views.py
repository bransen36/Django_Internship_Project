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
from django.utils import timezone
from django.template.loader import render_to_string


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

# All views that have to do with the list page. Add, Edit, Delete, etc..
class list_view(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/lists.html'

    def get(self, request):
        form = CreateTaskForm()
        tasks = request.user.tasks.all()
        return render(request, 'todo_list/lists.html', {'tasks': tasks, 'form': form})
        
    # View to add a new CheckList_Item to the database.
    def add_task(request):
        task = request.POST.get('task')
        description = request.POST.get('description')

        new_task = Checklist_Item.objects.create(
            task=task,
            description=description,
            created_at = timezone.now(),
            is_complete = False)

        # add the task to the user's list
        request.user.tasks.add(new_task)

        # return template with all of the user's films
        tasks = request.user.tasks.all()
        form = CreateTaskForm()

        # If HTMX, return only the fragment (no navbar)
        if request.headers.get('HX-Request'):
            html = render_to_string('todo_list/task_ui_partial.html', {'tasks': tasks, 'form': form}, request=request)
            return HttpResponse(html)
        
        return render(request, 'todo_list/lists.html', {'tasks': tasks, 'form': form})
    
    # View to mark a CheckList_Item as Complete or Incomplete using the Complete Task/Un-Complete button
    def complete_task(request):
        task_id = request.POST.get('id')

        task = Checklist_Item.objects.get(id=task_id, user=request.user)
        if task.is_complete:
            task.is_complete = False
            task.save()
        else:
            task.is_complete = True
            task.save()
        tasks = request.user.tasks.all()
        return render(request, 'todo_list/task_list.html', {'tasks': tasks})

    # View to delete a CheckList_Item
    def delete_task(request):
        task_id = request.POST.get('id')

        Checklist_Item.objects.filter(id=task_id).delete()

        tasks = request.user.tasks.all()
        form = CreateTaskForm()
        return render(request, 'todo_list/task_list.html', {'tasks': tasks, 'form': form})
    
    # View to edit a CheckList_Item
    def edit_task(request):
        task_id = request.POST.get('id') or request.GET.get('id')
        task = Checklist_Item.objects.filter(id=task_id).get()

        if request.method == 'POST':
            form = EditTaskForm(request.POST)
            if form.is_valid():
                task.task = form.cleaned_data['task']
                task.description = form.cleaned_data['description']
                task.is_complete = form.cleaned_data['is_complete']
                task.updated_at = timezone.now()
                task.save()
                return render(request, 'todo_list/task_list.html', {
                    'tasks': request.user.tasks.all(),
                    'form': CreateTaskForm()
                })  # Replace with your actual redirect target
            else:
                return HttpResponse("Invalid form submission")
        else:
            form = EditTaskForm(initial={
                'task': task.task,
                'description': task.description,
                'is_complete': str(task.is_complete),  # 'True' or 'False'
            })

        return render(request, 'todo_list/edit_task_form.html', {'form': form, 'task': task})
    


class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/dashboard.html'

# All views that have to do with the Profile page
class profile_view(LoginRequiredMixin, TemplateView):
    template_name = 'todo_list/profile.html'

    def get(self, request):
        user = request.user
        form = EditUserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'phone_number': user.phone_number,
            'address1': user.address1,
            'address2': user.address2
        }, instance=user)

        return render(request, 'todo_list/profile.html', {'form': form})
    
    def edit_profile(request):
        user = request.user
        form = EditUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            for field in form.fields.values():
                field.widget.attrs['disabled'] = 'disabled'

            html = render_to_string("todo_list/profile.html", {'form': form})
            return HttpResponse(html)

        return render(request, 'todo_list/profile.html', {'form': form})