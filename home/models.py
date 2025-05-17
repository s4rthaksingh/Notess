from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=5000)
    def __str__(self):
        return self.title