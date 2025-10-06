from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from django.contrib import messages

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
