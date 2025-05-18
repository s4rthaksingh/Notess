from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.index,name="index"),
    path('notes/<int:noteid>',views.viewnote,name='viewnote'),
    path('notebooks/<int:notebookid>',views.viewnotebook),
    path('create/',views.create,name='create'),
    path('create-notebook/',views.createnotebook,name='create'),
    path('delete-notebook/<int:notebookid>',views.deletenotebook),
    path('delete/<int:noteid>',views.delete),
    path('edit/<int:noteid>',views.edit),
    path('edit-notebook/<int:notebookid>',views.editnotebook),
    path('share/<int:noteid>',views.share),
    path('login/',views.loginUser),
    path('logout/',views.logoutUser),
    path('register/',views.register),
    path('users/',views.users),
    path('users/<username>',views.viewuser),
]
