from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Task
from django.utils import timezone
import time


class TaskAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Sample Task",
            description="Sample Description",
            due_date="2025-12-31"
        )

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2025-12-31"
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_invalid_due_date(self):
        data = {
            "title": "Invalid",
            "description": "No date",
            "due_date": "invalid-date"
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, 400)

    def test_list_tasks(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), Task.objects.count())

    def test_retrieve_valid_task(self):
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], self.task.title)

    def test_retrieve_invalid_task(self):
        response = self.client.get("/api/tasks/999/")
        self.assertEqual(response.status_code, 404)

    def test_update_status_valid(self):
        response = self.client.patch(f"/api/tasks/{self.task.id}/", {"status": "in_progress"})
        print("response", response.data)
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "in_progress")

    def test_update_status_invalid(self):
        response = self.client.patch(f"/api/tasks/{self.task.id}/", {"status": "invalid_status"})
        self.assertEqual(response.status_code, 400)

    def test_delete_valid_task(self):
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_invalid_task(self):
        response = self.client.delete("/api/tasks/999/")
        self.assertEqual(response.status_code, 404)

    def test_background_job_status_flow(self):
        data = {
            "title": "BG Task",
            "description": "Background processing",
            "due_date": "2025-12-31"
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, 201)

        task_id = response.data["id"]

        time.sleep(20)

        task = Task.objects.get(id=task_id)
        self.assertEqual(task.status, "completed")
