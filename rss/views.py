from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rss.models import Feed, FeedItem
from rss.serializers import FeedItemSerializer, FeedSerializer
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rss.tasks import update_single_feed
# Create your views here.


class FollowFeed(CreateAPIView):
    """
    follow and create new feed for user
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UnFollowFeed(DestroyAPIView):
    """
    unfollow and create new feed for user
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_object(self):
        obj = get_object_or_404(
            Feed, id=self.kwargs['pk'], user=self.request.user)
        return obj


class ListUserFeed(ListAPIView):
    """
    List all feeds followed by the user
    """
    permission_classes = [IsAuthenticated, ]
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)


class ListFeedItem(ListAPIView):
    """
    List feed items belonging to one feed
    """
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed_id=self.kwargs['pk'])


class UnReadItemList(ListAPIView):
    """
    Filter unread feed items globally 
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed__user=self.request.user, read=False).order_by('-date_fetched')


class ReadItemList(ListAPIView):
    """
    Filter read feed items globally 
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed__user=self.request.user, read=True).order_by('-date_fetched')


class UnReadFeedItemList(ListAPIView):
    """
    Filter unread feed items per feed
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed__user=self.request.user, read=False, feed=self.kwargs['pk']).order_by('-date_fetched')


class ReadFeedItemList(ListAPIView):
    """
    Filter read feed items per feed
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeedItemSerializer

    def get_queryset(self):
        return FeedItem.objects.filter(feed__user=self.request.user, read=True, feed=self.kwargs['pk']).order_by('-date_fetched')


class MakeReadItem(UpdateAPIView):
    """
    mark as read item with pk of item
    """
    queryset = FeedItem.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = FeedItemSerializer

    def update(self, request, *args, **kwargs):
        instance = FeedItem.objects.filter(
            id=self.kwargs['pk'], feed__user=self.request.user)
        if not instance.exists():
            return Response({"message": "Access Denied"}, status=status.HTTP_403_FORBIDDEN)
        instance.update(read=True)
        return Response({"message": "Item read successfully"}, status=status.HTTP_200_OK)


class ForceUpdateFeed(APIView):
    """
    fource update feed item with pk of feed
    """
    permission_classes = [IsAuthenticated, ]

    def post(self, request, pk):
        if Feed.objects.filter(id=pk).exists():
            update_single_feed.delay(pk)
            return Response({"message": "Feed Updated successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Feed Not Found"}, status=status.HTTP_404_NOT_FOUND)
