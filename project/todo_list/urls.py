from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view.as_view(), name='login'),
    path('sign_up/', views.signup_view.as_view(), name='sign_up'),
    path('lists/', views.list_view.as_view(), name='lists'),
    path('logout/', views.logout_view.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('tasks/', views.list_view.TaskList.as_view(), name='task_list')
]

htmx_urlpatterns = [
    path('check_username/', views.signup_view.check_username, name='check-username'),
    path('check_email/', views.signup_view.check_email, name="check-email"),
    path('add_task/', views.list_view.add_task, name='add_task')
]

urlpatterns += htmx_urlpatterns