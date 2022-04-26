from django.urls import path

from rss.views import FollowFeed, ForceUpdateFeed, ListUserFeed, UnFollowFeed, ListFeedItem, MakeReadItem, UnReadItemList, ReadItemList, UnReadFeedItemList, ReadFeedItemList


app_name = 'rss'

urlpatterns = [

    path('follow/', FollowFeed.as_view(), name='followfeed'),
    path('unfollow/<int:pk>/', UnFollowFeed.as_view(), name='unfollowfeed'),
    path('list/', ListUserFeed.as_view(), name='listfeed'),
    path('feed/<int:pk>/', ListFeedItem.as_view(), name='feeditem'),
    path('feed/action/read/<int:pk>/', MakeReadItem.as_view(), name='readitem'),
    path('unread/', UnReadItemList.as_view(), name='unreaditemlist'),
    path('read/', ReadItemList.as_view(), name='readitemlist'),
    path('feed/unread/<int:pk>/', UnReadFeedItemList.as_view(),
         name='unreadfeeditemlist'),
    path('feed/read/<int:pk>/', ReadFeedItemList.as_view(), name='readfeeditemlist'),
    path('feed/update/<int:pk>/', ForceUpdateFeed.as_view(), name='forceupdatefeed'),
]
