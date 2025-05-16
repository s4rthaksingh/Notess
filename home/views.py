from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Note
from .forms import NoteForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url="/login")
def index(request):
    context={
        'user' : request.user,
        'notes': Note.objects.filter(user=request.user),
    }
    return render(request,'index.html',context=context)

@login_required(login_url="/login")
def viewnote(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    context={
        'note' : Note.objects.get(pk=noteid)
    }
    return render(request,'viewnote.html',context=context)

@login_required(login_url="/login")
def create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return HttpResponseRedirect("/")  
    else:
        form = NoteForm()
    return render(request,'create.html',{'form':form})

@login_required(login_url="/login")
def delete(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    else:
        Note.objects.get(pk=noteid).delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
def edit(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    if request.method == 'POST':
        form = NoteForm(request.POST,instance=Note.objects.get(pk=noteid))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = NoteForm(instance=Note.objects.get(pk=noteid))
    return render(request,'edit.html',{'form':form})

def loginUser(request):
    if request.user.is_authenticated:
        return render(request,'already.html',{'title':'Log in to another account','action':'log in to another account'})
    if request.method=='POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password").lower()
        if not User.objects.filter(username=username):
            messages.error(request,"Invalid username")
            return HttpResponseRedirect('/login')
        
        user = authenticate(username=username,password=password)

        if user is None:
            messages.error(request,"Invalid password")
            return HttpResponseRedirect('/login')
        else:
            login(request,user)
            return HttpResponseRedirect('/')
    return render(request,'login.html')

@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated:
        return render(request,'already.html',{'title':'Register a new account','action':'register a new account'})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return HttpResponseRedirect('/')
    else:
        form = RegisterForm()
    return render(request,'register.html',{'form':form})