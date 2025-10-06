from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    
    path('projects/add/', views.project_create, name='create_project'),
    path('projects/<int:pk>/edit/', views.edit_project, name='project_edit'),
    
    path('tasks/add/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
]
