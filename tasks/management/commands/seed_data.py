from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from tasks.models import Comment, Project, Task

User = get_user_model()

SAMPLE_TASKS = [
    ("Set up Django project", Task.Status.DONE, Task.Priority.HIGH),
    ("Design the task models", Task.Status.DONE, Task.Priority.HIGH),
    ("Build the task API", Task.Status.IN_PROGRESS, Task.Priority.HIGH),
    ("Test CRUD operations", Task.Status.TODO, Task.Priority.MEDIUM),
    ("Write the README", Task.Status.TODO, Task.Priority.LOW),
]


class Command(BaseCommand):
    help = "Create a demo user, project, tasks and a comment."

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(
            username="demo_user", defaults={"email": "demo@example.com"}
        )
        user.set_password("demo-password-123")
        user.save()

        project, _ = Project.objects.get_or_create(
            name="Task Tracker Demo",
            defaults={"summary": "Sample project for the API", "owner": user},
        )
        for title, status, priority in SAMPLE_TASKS:
            task, _ = Task.objects.get_or_create(
                title=title,
                project=project,
                defaults={
                    "details": title,
                    "assignee": user,
                    "status": status,
                    "priority": priority,
                },
            )
            if status == Task.Status.DONE:
                Comment.objects.get_or_create(
                    task=task, author=user, text="Finished and checked."
                )
        self.stdout.write(self.style.SUCCESS("Sample data created."))
