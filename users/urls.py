from django.urls import include, path

from .views import UserListView, getCurrentProfile, setProfilePicture, setProfileBio, getGlobalUsersByNameSearch

urlpatterns = [
    path('', UserListView.as_view()),
    path('get_current_profile', getCurrentProfile),
    path('set_profile_picture', setProfilePicture),
    path('set_profile_bio', setProfileBio),
    path('search_global_users',getGlobalUsersByNameSearch),
]
