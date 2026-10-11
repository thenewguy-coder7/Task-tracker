from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    assignee_username = serializers.CharField(
        source="assignee.username", read_only=True, default=None
    )
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "details",
            "project",
            "project_name",
            "assignee",
            "assignee_username",
            "status",
            "priority",
            "due_date",
            "is_overdue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value):
        value = value.strip()
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters.")
        return value

    def validate_due_date(self, value):
        # Only block past dates when a task is being created.
        if self.instance is None and value and value < timezone.localdate():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
