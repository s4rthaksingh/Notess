from django import forms
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','description']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']