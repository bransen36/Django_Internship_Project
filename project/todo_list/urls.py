from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view.as_view(), name='login'),
    path('sign_up/', views.signup_view.as_view(), name='sign_up'),
    path('lists/', views.list_view.as_view(), name='lists'),
    path('logout/', views.logout_view.as_view(next_page='index'), name='logout'),
    path('dashboard/', views.dashboard.as_view(), name='dashboard'),
    path('profile/', views.profile_view.as_view(), name='profile')
]

htmx_urlpatterns = [
    path('check_username/', views.signup_view.check_username, name='check-username'),
    path('check_email/', views.signup_view.check_email, name="check-email"),
    path('add_task/', views.list_view.add_task, name='add_task'),
    path('complete_task/', views.list_view.complete_task, name='complete_task'),
    path('delete_task/', views.list_view.delete_task, name='delete_task'),
    path('edit_task/', views.list_view.edit_task, name='edit_task'),
    path('edit_profile/', views.profile_view.edit_profile, name='edit_profile')
]

urlpatterns += htmx_urlpatterns