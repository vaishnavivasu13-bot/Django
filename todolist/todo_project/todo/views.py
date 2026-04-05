from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('tasks')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def tasks(request):
    if request.method == 'POST':
        Task.objects.create(user=request.user, title=request.POST['title'])
        return redirect('tasks')
    
    user_tasks = Task.objects.filter(user=request.user)
    pending = user_tasks.filter(completed=False)
    completed = user_tasks.filter(completed=True)
    
    return render(request, 'tasks.html', {'pending': pending, 'completed': completed})

@login_required
def complete_task(request, task_id):
    Task.objects.get(id=task_id, user=request.user).completed = True
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id, user=request.user).delete()
    return redirect('tasks')