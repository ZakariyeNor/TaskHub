from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task, ActivityLog
from django.contrib import messages
from .forms import ProjectForm, TaskForm

# -----------------------
# Project List View
# -----------------------
@login_required
def project_list(request):
    projects = Project.objects.filter(owner=request.user) | Project.objects.filter(members=request.user)
    return render(request, 'core/project_list.html', {'projects': projects})


# -----------------------
# Project Detail View
# -----------------------
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, 'core/project_detail.html', {'project': project, 'tasks': tasks})

# Create Project
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(
        request,
        'core/project_form.html',
        {
            "form": form,
            'title': 'Create Project'
        }
    )

# Edit project
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form, 'title': 'Edit Project'})



# -----------------------
# Task Detail View
# -----------------------
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'core/task_detail.html', {'task': task})


# -----------------------
# Mark Task as Done
# -----------------------
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user == task.assigned_to or request.user == task.project.owner:
        task.status = 'done'
        task.save()
        messages.success(request, f"Task '{task.title}' marked as done.")
    else:
        messages.error(request, "You don't have permission to complete this task.")
    return redirect('project_detail', project_id=task.project.id)


# Create a task
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form, 'title': 'Create Task'})

# Edit task 
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def activity_feed(request):
    logs = ActivityLog.objects.filter(user=request.user)
    return render(request, 'core/activity_feed.html', {'logs': logs})