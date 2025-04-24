from django.urls import path

from .views import (
    FriendListView,
    FriendRequestListView,
    SendFriendRequestView,
    RespondToFriendRequestView,
    FriendSuggestionView,
)

urlpatterns = [
    path('', FriendListView.as_view(), name='friend-list'),
    path('requests/', FriendRequestListView.as_view(), name='friend-request-list'),
    path('requests/<int:user_id>/', SendFriendRequestView.as_view(),
         name='send-friend-request'),
    path('requests/<int:request_id>/accept/',
         RespondToFriendRequestView.as_view(),
         {'action': 'accept'},
         name='accept-friend-request'
         ),
    path('requests/<int:request_id>/reject/',
         RespondToFriendRequestView.as_view(),
         {'action': 'reject'},
         name='reject-friend-request'
         ),
    path('suggestions/', FriendSuggestionView.as_view(), name='friend-suggestions'),
]
