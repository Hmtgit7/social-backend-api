from django.contrib import admin
from .models import FriendRequest, Friendship


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    """Admin configuration for the FriendRequest model."""
    
    list_display = ('id', 'sender', 'receiver', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('sender__email', 'sender__name', 'receiver__email', 'receiver__name')
    raw_id_fields = ('sender', 'receiver')
    list_per_page = 20


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    """Admin configuration for the Friendship model."""
    
    list_display = ('id', 'user1', 'user2', 'created_at')
    search_fields = ('user1__email', 'user1__name', 'user2__email', 'user2__name')
    raw_id_fields = ('user1', 'user2')
    list_per_page = 20