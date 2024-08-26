from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_tasks')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    not_deleted = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
