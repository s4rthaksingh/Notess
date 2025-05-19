from django.contrib import admin

# Register your models here.
from .models import Note,Activity,Notebook

admin.site.register(Note)
admin.site.register(Notebook)
admin.site.register(Activity)