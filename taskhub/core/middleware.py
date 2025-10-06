import datetime
from django.utils.deprecation import MiddlewareMixin

class SimpleLoggingMiddleware(MiddlewareMixin):
    """
    Logs basic info about each request.
    """
    def process_request(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        method = request.method
        timestamp = datetime.datetime.now()
        print(f"[{timestamp}] {method} request to {path} by {user}")

class ProjectAccessMiddleware(MiddlewareMixin):
    """
    Restrict access to projects to members only.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        project_id = view_kwargs.get('project_id')
        if project_id and request.user.is_authenticated:
            from .models import Project
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("Project not found.")
            
            if request.user not in project.members.all() and request.user != project.owner:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden("You do not have access to this project.")
