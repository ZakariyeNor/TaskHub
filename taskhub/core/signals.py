from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Task, Project

# -------------
# Task Signals
# -------------

# Notify when a task is created or updated
@receiver(post_save, sender=Task)
def task_created_updated(sender, instance, created, **kwargs):
    if created:
        print(
            f"Task '{instance.title}' created in project '{instance.project.name}'"
        # Here, you could send an email or push notification
        )
    else:
        print(
            f"Task '{instance.title}' updated in project '{instance.project.name}'"
        # Optional: send update notification
        )


# Log task deletion
@receiver(pre_delete, sender=Task)
def task_deleted(sender, instance, created, **kwargs):
    if created:
        print(
            f"Task '{instance.title}' deleted from project '{instance.project.name}'"
        )

# -----------------------
# Project Signals
# -----------------------
@receiver(post_save, sender=Project)
def project_created_updated(sender, instance, created, **kwargs):
    if created:
        print(
            f"Project '{instance.name}' created by '{instance.project.username}'"
        )
    else:
        print(
            f"Project '{instance.name}' updated"
        )