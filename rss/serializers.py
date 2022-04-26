from rest_framework import serializers
from rss.models import Feed, FeedItem


class FeedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feed
        fields = ('id', 'title', 'link')


class FeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedItem
        fields = ('id', 'title', 'link', 'context', 'read', 'date_publish')
