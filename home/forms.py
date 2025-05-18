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
        fields = ["name","is_public"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Remove 'user' from kwargs and assign it
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        is_public = cleaned_data.get('is_public')
        if is_public:
            already_public = Notebook.objects.filter(user=self.user,is_public=True).exclude(pk=self.instance.pk).exists()
            if already_public:
                raise forms.ValidationError("You already have a public notebook, make it private first")
        return cleaned_data
