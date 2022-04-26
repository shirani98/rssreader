from django.db import models
from django.contrib.auth.models import User
import feedparser

# Create your models here.


class Feed(models.Model):
    """
    feed model
    """
    title = models.CharField(max_length=250, blank=True, null=True)
    link = models.CharField(max_length=450)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="userfeed", blank=True, null=True)
    last_update = models.DateTimeField(editable=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link

    def update_feed(self):
        """
        update feed and save items in FeedItem model as unread items.
        """
        feed = feedparser.parse(self.link)
        for item in feed['entries']:
            if not FeedItem.objects.filter(link=item['link']).exists():
                #time = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S GMT').strftime("%Y-%m-%d %H:%M:%S")
                FeedItem.objects.create(
                    title=item['title'], link=item['link'], context=item['summary'], date_publish=item['published'], feed=self)


class FeedItem(models.Model):
    """
    feed item model
    """
    title = models.CharField(max_length=400, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    context = models.TextField(null=True, blank=True)
    feed = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name='feed')
    read = models.BooleanField(default=False)
    date_fetched = models.DateTimeField(auto_now_add=True)
    date_publish = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def mark_as_read(self):
        """
        Mark an item as read.
        """
        self.read = True
        self.save()
