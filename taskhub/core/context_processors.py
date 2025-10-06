from .models import Task

def global_context(request):
    """
    Provides global data (visible in all templates).
    """
    user = request.user
    context = {}
    
    if user.is_authenticated:
        # Example: count of assigned tasks not marked done
        pending_tasks = Task.objects.filter(assigned_to=user, status__in=['todo', 'in_progress']).count()
        
        # Example notification placeholder
        notifications = [
            {"message": "New task assigned", "type": "info"},
            {"message": "Project deadline approaching", "type": "warning"},
        ]
        
        context.update({
            'pending_tasks': pending_tasks,
            'notifications': notifications,
            'username': user.username,
        })

    return context