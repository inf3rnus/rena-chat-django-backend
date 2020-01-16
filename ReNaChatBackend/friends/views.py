from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import UserSerializer
from users.forms import CustomUserDetailsForm

from friends.models import Friend
from friends.serializers import FriendSerializer

# Create your views here.

@api_view(['post'])
@permission_classes([IsAuthenticated])
def requestFriend(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[requestFriend] - User <', serializer.data['username'], '> is trying to make a friend request to ', request.POST.get('username', ''))

    if form.is_valid():
        new_friend = CustomUser.objects.get(username=form.cleaned_data['username'])
        Friend.add_pending_friend(request.user, new_friend)

        return Response({"success": "true", "current_user": serializer.data['username']})

    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def removeRequestedFriend(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[requestFriend] - User <', serializer.data['username'], '> is trying to make a friend request to ', request.POST.get('username', ''))

    if form.is_valid():
        new_friend = CustomUser.objects.get(username=form.cleaned_data['username'])
        Friend.remove_requested_friend(request.user, new_friend)

        return Response({"success": "true", "current_user": serializer.data['username']})

    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def removePendingFriend(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[requestFriend] - User <', serializer.data['username'], '> is trying to make a friend request to ', request.POST.get('username', ''))

    if form.is_valid():
        new_friend = CustomUser.objects.get(username=form.cleaned_data['username'])
        Friend.remove_pending_friend(request.user, new_friend)

        return Response({"success": "true", "current_user": serializer.data['username']})

    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def confirmFriend(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[confirmFriend] - User <', serializer.data['username'], '> is trying to make approve a friend request to ', request.POST.get('username', ''))

    if form.is_valid():
        new_friend = CustomUser.objects.get(username=form.cleaned_data['username'])
        Friend.confirm_friend(request.user, new_friend)

        return Response({"success": "true", "current_user": serializer.data['username']})

    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def removeFriend(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[requestFriend] - User <', serializer.data['username'], '> is trying to remove friend:', request.POST.get('username', ''))

    if form.is_valid():
        new_friend = CustomUser.objects.get(username=form.cleaned_data['username'])
        Friend.remove_friend(request.user, new_friend)

        return Response({"success": "true", "current_user": serializer.data['username']})

    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getPendingFriends(request):
    friendObj = Friend.objects.get(user_profile_id=request.user.id)
    pendingFriendUserList = friendObj.pending_friends.all()
    serializer = UserSerializer(pendingFriendUserList, many=True)
    return Response(serializer.data)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getRequestedFriends(request):
    friendObj = Friend.objects.get(user_profile_id=request.user.id)
    pendingFriendUserList = friendObj.requested_friends.all()
    serializer = UserSerializer(pendingFriendUserList, many=True)
    return Response(serializer.data)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getFriends(request):
    friendObj = Friend.objects.get(user_profile_id=request.user.id)
    friendUserList = friendObj.friends.all()
    serializer = UserSerializer(friendUserList, many=True)
    return Response(serializer.data)