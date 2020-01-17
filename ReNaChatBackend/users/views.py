from rest_framework import generics

from . import models
from . import serializers

class UserListView(generics.ListAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

@api_view(['get'])
@permission_classes([IsAuthenticated])
def getCurrentProfile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
    print("Form errors: ", form.errors)
    return HttpResponse(status=500)

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