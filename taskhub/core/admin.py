from django.contrib import admin
from .models import Project, Task, TaskMetadata

class TaskMetadataInline(admin.TabularInline):
    model = TaskMetadata
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project')
    inlines = [TaskMetadataInline]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    filter_horizontal = ('members',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
