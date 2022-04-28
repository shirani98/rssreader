import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rssreader.settings')

app = Celery('rssreader',broker='amqp://guest:guest@rabbitmq3:5672/')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-every-60-seconds': {
        'task': 'rss.tasks.update_all_feeds',
        'schedule': 60.0
    },
}