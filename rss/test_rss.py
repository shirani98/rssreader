import pytest
from django.contrib.auth.models import User
from rss.models import Feed, FeedItem


@pytest.mark.django_db
def test_update_feed():
    feed = Feed.objects.create(link='https://www.varzesh3.com/rss/all')
    feed.update_feed()
    assert FeedItem.objects.all().count() == 40


@pytest.mark.django_db
def test_mark_read():
    feed = Feed(link='https://www.varzesh3.com/rss/all')
    feed.save()
    feed.update_feed()
    assert FeedItem.objects.filter(read=False).count() == 40

    for item in FeedItem.objects.filter(read=False):
        item.mark_as_read()
    assert FeedItem.objects.filter(read=False).count() == 0


@pytest.mark.django_db
def test_users_feeds():
    user1 = User(username="user1")
    user1.set_unusable_password()
    user1.save()
    user2 = User(username="user2")
    user2.set_unusable_password()
    user2.save()

    feed_url = 'https://www.varzesh3.com/rss/all'
    feed1 = Feed.objects.create(user=user1, link=feed_url)
    feed2 = Feed.objects.create(user=user2, link=feed_url)
    assert feed1.link != None
    assert feed2.link != None
