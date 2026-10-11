from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Full CRUD for tasks: list, create, retrieve, update, partial update, delete.

    Optional query parameters on the list endpoint:
    ?project=<id>  ?status=TODO  ?priority=HIGH  ?search=<text in title>
    """

    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.select_related("project", "assignee")
        params = self.request.query_params
        for field in ("project", "status", "priority"):
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        search = params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """POST /api/tasks/<id>/complete/ - shortcut to mark a task as done."""
        task = self.get_object()
        task.status = Task.Status.DONE
        task.save(update_fields=["status", "updated_at"])
        return Response(self.get_serializer(task).data)
