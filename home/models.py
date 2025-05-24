from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
import pytz

IST = pytz.timezone('Asia/Kolkata')
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
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        ist_time = localtime(self.time,timezone=IST)
        return f"{self.user} {self.message} on {ist_time.strftime("%B %d, %Y")}\n at {ist_time.strftime("%I:%M:%S %p")}"