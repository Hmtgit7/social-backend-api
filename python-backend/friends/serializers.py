from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import FriendRequest, Friendship
from accounts.serializers import UserListSerializer

User = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for the FriendRequest model."""
    
    sender = UserListSerializer(read_only=True)
    receiver = UserListSerializer(read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'sender', 'status', 'created_at', 'updated_at']


class FriendshipSerializer(serializers.ModelSerializer):
    """Serializer for the Friendship model."""
    
    friend = serializers.SerializerMethodField()
    
    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'created_at']
        read_only_fields = ['id', 'friend', 'created_at']
    
    def get_friend(self, obj):
        """Return the friend of the current user."""
        request = self.context.get('request')
        if request and request.user:
            user = request.user
            friend = obj.user2 if user == obj.user1 else obj.user1
            return UserListSerializer(friend).data
        return None


class FriendSuggestionSerializer(serializers.ModelSerializer):
    """Serializer for friend suggestions."""
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'profile_picture']
        read_only_fields = ['id', 'name', 'email', 'profile_picture']