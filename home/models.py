from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    def __str__(self):
        return self.title
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.message} at {self.time.strftime('%I:%M %p')}"