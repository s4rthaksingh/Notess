from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Note,Notebook
from .forms import NoteForm, RegisterForm,NotebookForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url="/login")
def index(request):
    context={
        'user' : request.user,
        'notebooks': Notebook.objects.filter(user=request.user),
    }
    return render(request,'viewnotebooks.html',context=context)

@login_required(login_url="/login")
def viewnote(request,noteid):
    note = Note.objects.get(pk=noteid)
    if request.user != note.user and not note.notebook.is_public:
        return HttpResponse("This note doesn't exist")
    context={
        'note' : note
    }
    return render(request,'viewnote.html',context=context)

@login_required(login_url="/login")
def viewnotebook(request,notebookid):
    if request.user != Notebook.objects.get(pk=notebookid).user:
        return HttpResponse("This note doesn't exist")
    notebook = Notebook.objects.get(pk=notebookid)
    context={
        'notes' : Note.objects.filter(notebook=notebook),
        'user' : request.user
    }
    return render(request,'index.html',context=context)


@login_required(login_url="/login")
def create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST,user=request.user)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return HttpResponseRedirect("/")  
    else:
        form = NoteForm(user=request.user)
    return render(request,'create.html',{'form':form})

@login_required(login_url="/login")
def createnotebook(request):
    if request.method == 'POST':
        form = NotebookForm(request.POST,user=request.user)
        if form.is_valid():
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()
            return HttpResponseRedirect("/")
    else:
        form = NotebookForm(user=request.user)
    return render(request,'createnotebook.html',{'form':form})

@login_required(login_url="/login")
def delete(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    else:
        Note.objects.get(pk=noteid).delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
def deletenotebook(request,notebookid):
    if request.user != Notebook.objects.get(pk=notebookid).user:
        return HttpResponse("This note doesn't exist")
    else:
        Notebook.objects.get(pk=notebookid).delete()
    return HttpResponseRedirect('/')

@login_required(login_url="/login")
def edit(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    if request.method == 'POST':
        form = NoteForm(request.POST,instance=Note.objects.get(pk=noteid),user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = NoteForm(instance=Note.objects.get(pk=noteid),user=request.user)
    return render(request,'edit.html',{'form':form})

@login_required(login_url="/login")
def editnotebook(request,notebookid):
    if request.method == 'POST':
        form = NotebookForm(request.POST,instance=Notebook.objects.get(pk=notebookid),user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = NotebookForm(instance=Notebook.objects.get(pk=notebookid),user=request.user)
    return render(request,'editnotebook.html',{'form':form})

@login_required
def share(request,noteid):
    if request.user != Note.objects.get(pk=noteid).user:
        return HttpResponse("This note doesn't exist")
    if request.method=='POST':
        user_id = int(request.POST['dropdown'])
        user = User.objects.all().get(pk=user_id)
        note = Note.objects.get(pk=noteid)
        notebook,created = Notebook.objects.get_or_create(
            name=f"Shared by {note.user}",
            user=user
        )
        newnote = Note(title=f'{note.title} - Shared by {note.user}',description=note.description,user=user,notebook=notebook)
        newnote.save()
        return HttpResponse(f'Successfully shared note "{Note.objects.get(pk=noteid)}" with {user.username}')
    else:
        return render(request,'share.html',{'users':User.objects.all()})

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

def users(request):
    users = User.objects.all()
    return render(request,'users.html',{'users':users})

def viewuser(request,username):
    print(username)
    user = User.objects.get(username=username)
    print(user)
    public_notebook = Notebook.objects.filter(user=user,is_public=True).first()
    print(public_notebook)
    notes = Note.objects.filter(user=user,notebook=public_notebook)
    return render(request,'profile.html',{'notebook':public_notebook,'notes':notes,'user':user})