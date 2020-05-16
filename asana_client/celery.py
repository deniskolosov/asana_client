from celery import Celery

app = Celery(
    'asana_client',
    broker='amqp://guest:guest@rabbit:5672//',
    # include=['manager.tasks']
)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update({
    'result_persistent': True,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']})
app.autodiscover_tasks()
