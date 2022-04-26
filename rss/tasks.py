from celery import Celery, shared_task
from rss.models import Feed


@shared_task(retry_backoff=True, retry_kwargs={'max_retries': 5})
def update_all_feeds():

    for feed in Feed.objects.all():
        feed.update_feed()


@shared_task(retry_backoff=True, retry_kwargs={'max_retries': 5})
def update_single_feed(pk):
    Feed.objects.get(id=pk).update_feed()
