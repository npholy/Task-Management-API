from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm  # We’ll create this form next

def task_list_view(request):
    tasks = Task.objects.filter(user=request.user)  # Show only user's tasks
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_create_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list-ui')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_create.html', {'form': form})

def task_update_view(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list-ui')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_update.html', {'form': form})
