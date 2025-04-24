"""
URL configuration for social_backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/users/', include('accounts.user_urls')),
    path('api/friends/', include('friends.urls')),
]