from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(("This is the first name of the user"), max_length=50)
    last_name = models.CharField(("This is the last name of the user"), max_length=50)
    
class Checklist_Item():
    User = User
    created_at = models.DateTimeField(("The date and time that the item was created"), auto_now=True)
    is_complete = models.BooleanField(("Has the task been completed or not"))
