from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name="index"),
    path('notes/<int:noteid>',views.viewnote,name='viewnote'),
    path('create/',views.create,name='create'),
    path('delete/<int:noteid>',views.delete),
    path('edit/<int:noteid>',views.edit),
    path('share/<int:noteid>',views.share),
    path('login/',views.loginUser),
    path('logout/',views.logoutUser),
    path('register/',views.register)
]
