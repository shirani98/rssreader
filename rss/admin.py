from django.contrib import admin

from rss.models import FeedItem, Feed

# Register your models here.

admin.site.register(Feed)
admin.site.register(FeedItem)