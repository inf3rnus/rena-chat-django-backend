from django.urls import include, path

from .views import UserListView, getCurrentProfile, setProfilePicture, setProfileBio

urlpatterns = [
    path('', UserListView.as_view()),
    path('get_current_profile', getCurrentProfile),
    path('set_profile_picture', setProfilePicture),
    path('set_profile_bio', setProfileBio),
]
