# api/urls.py
from django.urls import include, path
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('chat/', include('chat.urls')),
    path('users/', include('users.urls')),
    path('friends/', include('friends.urls')),
    path('rest-auth/refresh_jwt/', refresh_jwt_token),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]