import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from rss.models import Feed, FeedItem
from rss.tasks import update_single_feed


class FeedType(DjangoObjectType):
    class Meta:
        model = Feed


class FeedItemType(DjangoObjectType):
    class Meta:
        model = FeedItem


class UpdateReadItem(graphene.Mutation):
    #mark as read item
    class Arguments:
        id = graphene.ID(required=True)

    feeditem = graphene.Field(FeedItemType)

    @classmethod
    def mutate(cls, root, info, id):
        instance = FeedItem.objects.filter(
            id=id, feed__user=info.context.user)
        if instance.exists():
            instance.mark_as_read()
            return UpdateReadItem(feeditem=instance)
        return None

class FourceUpdateItem(graphene.Mutation):
    #fource update feed item
    class Arguments:
        id = graphene.ID(required=True)

    feed = graphene.List(FeedType)

    @classmethod
    def mutate(cls, root, info, id):
        feed = Feed.objects.filter(id=id)
        if feed.exists():
            update_single_feed.delay(id)
            return FourceUpdateItem(feed=feed)
        return None


class FollowFeed(graphene.Mutation):
    #follow and create new feed for user
    class Arguments:
        title = graphene.String()
        link = graphene.String(required=True)

    feed = graphene.Field(FeedType)

    @classmethod
    def mutate(cls, root, info, title, link):
        instance = Feed.objects.create(
            title=title, link=link, user=info.context.user)
        return FollowFeed(feed=instance)


class UnFollowFeed(graphene.Mutation):
    #unfollow and delete user feed
    class Arguments:
        id = graphene.ID(required=True)

    feed = graphene.Field(FeedType)

    @classmethod
    def mutate(cls, root, info, id):
        instance = Feed.objects.get(id=id)
        if instance.user == info.context.user:
            instance.delete()
            return FollowFeed(feed=instance)


class Mutation(graphene.ObjectType):
    makeread = UpdateReadItem.Field()
    forceupdate = FourceUpdateItem.Field()
    follow = FollowFeed.Field()
    unfollow = UnFollowFeed.Field()


class Query(ObjectType):
    followfeedlist = graphene.List(
        FeedType, username=graphene.String(required=True))
    feeditems = graphene.List(FeedItemType, feedid=graphene.Int(required=True))
    readfeeditemlist = graphene.List(
        FeedItemType, feedid=graphene.Int(required=True))
    unreadfeeditemlist = graphene.List(
        FeedItemType, feedid=graphene.Int(required=True))
    readitemlist = graphene.List(FeedItemType)
    unreaditemlist = graphene.List(FeedItemType)
    forceupdate = graphene.Field(FeedType, feedid=graphene.Int(required=True))

    def resolve_followfeedlist(parent, info, **kwargs):
        #List all feeds followed by the user
        return Feed.objects.filter(user__username=kwargs.get('username'))

    def resolve_feeditems(parent, info, **kwargs):
        #List feed items belonging to one feed
        return FeedItem.objects.filter(feed_id=kwargs.get('feedid'))

    def resolve_readfeeditemlist(parent, info, **kwargs):
        #Filter read feed items per feed 
        return FeedItem.objects.filter(read=True, feed_id=kwargs.get('feedid')).order_by('-date_fetched')

    def resolve_unreadfeeditemlist(parent, info, **kwargs):
        #Filter unread feed items per feed 
        return FeedItem.objects.filter(read=False, feed_id=kwargs.get('feedid')).order_by('-date_fetched')

    def resolve_readitemlist(parent, info, **kwargs):
        #Filter read feed items globally 
        return FeedItem.objects.filter(read=True).order_by('-date_fetched')

    def resolve_unreaditemlist(parent, info, **kwargs):
        #Filter unread feed items globally 
        return FeedItem.objects.filter(read=False).order_by('-date_fetched')
