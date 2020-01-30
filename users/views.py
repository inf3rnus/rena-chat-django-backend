from django.http import HttpResponse

from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .forms import CustomUserDetailsForm
from .serializers import UserSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getCurrentProfile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def setProfilePicture(request):
    form = CustomUserDetailsForm(request.POST, request.FILES)
    serializer = UserSerializer(request.user, many=False)
    print('[setProfilePicture] - User <', serializer.data['username'], '> is trying to set its profile picture.')
    if form.is_valid():
        request.user.profile_picture = form.cleaned_data['profile_picture']
        request.user.save()
        return Response({'success':'true', 'path': str(request.user.profile_picture)})
    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['post'])
@permission_classes([IsAuthenticated])
def setProfileBio(request):
    form = CustomUserDetailsForm(request.POST)
    serializer = UserSerializer(request.user, many=False)
    print('[setProfileBio] - User <', serializer.data['username'], '> is trying to set its bio.')
    if form.is_valid():
        request.user.bio = form.cleaned_data['bio']
        request.user.save()
        return Response({'success':'true', 'bio': request.user.bio})
    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getGlobalUsersByNameSearch(request):
    try:
        user_query_set = CustomUser.objects.filter(username__regex=r'^' + request.GET.get('username', None))
        serializer = UserSerializer(user_query_set, many=True)
        return Response(serializer.data)
    except:
        return HttpResponse(status=422)

