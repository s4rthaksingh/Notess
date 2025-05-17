from django import forms
from .models import Note,Notebook
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','description','notebook']
    
    def __init__(self,*args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['notebook'].queryset = Notebook.objects.filter(user=user)

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class NotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ["name"]