from django.urls import include, path

from friends.views import getPendingFriends
from friends.views import getFriends
from friends.views import requestFriend
from friends.views import confirmFriend
from friends.views import removeFriend
from friends.views import removePendingFriend
from friends.views import removeRequestedFriend
from friends.views import getRequestedFriends

urlpatterns = [
    path('get_pending_friends', getPendingFriends),
    path('get_requested_friends', getRequestedFriends),
    path('remove_pending_friend', removePendingFriend),
    path('remove_requested_friend', removeRequestedFriend),
    path('request_friend', requestFriend),
    path('confirm_friend', confirmFriend),
    path('remove_friend', removeFriend),
    path('get_friends', getFriends),
]

