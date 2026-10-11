from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project, Task

User = get_user_model()


class TaskApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pass12345")
        self.project = Project.objects.create(name="P1", owner=self.user)
        self.task = Task.objects.create(title="First task", project=self.project)

    def test_create_task(self):
        resp = self.client.post(
            "/api/tasks/",
            {"title": "New task", "project": self.project.id, "priority": "HIGH"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["status"], "TODO")
        self.assertEqual(resp.data["project_name"], "P1")

    def test_list_and_filter(self):
        Task.objects.create(
            title="Other", project=self.project, status=Task.Status.DONE
        )
        resp = self.client.get("/api/tasks/", {"status": "DONE"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data), 1)
        resp = self.client.get("/api/tasks/", {"search": "first"})
        self.assertEqual(len(resp.data), 1)

    def test_retrieve_update_delete(self):
        url = f"/api/tasks/{self.task.id}/"
        self.assertEqual(self.client.get(url).status_code, 200)
        resp = self.client.patch(url, {"status": "IN_PROGRESS"})
        self.assertEqual(resp.data["status"], "IN_PROGRESS")
        resp = self.client.put(
            url, {"title": "Renamed task", "project": self.project.id}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_past_due_date_rejected_on_create(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        resp = self.client.post(
            "/api/tasks/",
            {"title": "Late", "project": self.project.id, "due_date": yesterday},
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("due_date", resp.data)

    def test_complete_action(self):
        resp = self.client.post(f"/api/tasks/{self.task.id}/complete/")
        self.assertEqual(resp.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.DONE)
