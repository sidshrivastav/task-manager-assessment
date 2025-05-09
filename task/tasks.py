from celery import shared_task
import time
from .models import Task

@shared_task
def process_task(task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'in_progress'
        task.save()
        time.sleep(5)

        task.status = 'completed'
        task.save()

    except Task.DoesNotExist:
        pass