from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(("This is the first name of the user"), max_length=50)
    last_name = models.CharField(("This is the last name of the user"), max_length=50)
    
class Checklist_Item(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ManyToManyField(User, related_name='tasks') # related_name lets us do user.tasks.all()
    task = models.CharField(("The task to be completed for this checklist item."), max_length=100)
    description = models.TextField(("Long description of what the task is"), null=True)
    created_at = models.DateTimeField(("The date and time that the item was created"), auto_now=True)
    is_complete = models.BooleanField(("Has the task been completed or not"))
