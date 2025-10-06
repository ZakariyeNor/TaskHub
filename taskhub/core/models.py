from django.db import models
from django.contrib.auth.models import User


# Project model
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    members = models.ManyToManyField(User, related_name='shared_projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Task model 
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.IntegerField(default=0)  # 0 = low, 1 = medium, 2 = high
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return self.title


# Task metadata
class TaskMetadata(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='metadata')
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key}: {self.value}"


# ActiveLog and notifications
class ActivityLog(models.Model):
    ACTIONS = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('completed', 'Completed'),
        ('deleted', 'Deleted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=50)  # e.g., Project or Task
    object_id = models.IntegerField()               # ID of Project/Task
    action = models.CharField(max_length=20, choices=ACTIONS)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} {self.action} {self.content_type} {self.object_id}"