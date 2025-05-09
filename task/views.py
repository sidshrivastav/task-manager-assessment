from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .tasks import process_task

class TaskViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        task = serializer.save()
        process_task.delay(task.id)

    def perform_update(self, serializer):
        instance = self.get_object()
        old_status = instance.status
        task = serializer.save()
        if old_status != task.status and task.status == 'pending':
            process_task.delay(task.id)