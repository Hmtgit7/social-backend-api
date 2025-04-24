import pytest
from django.urls import reverse
from django.db.models import Q
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from friends.models import FriendRequest, Friendship

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email='user@example.com', password='password123', name='Test User'):
        return User.objects.create_user(
            email=email,
            password=password,
            name=name
        )
    return _create_user

@pytest.fixture
def create_friendship(create_user):
    def _create_friendship(user1=None, user2=None):
        if user1 is None:
            user1 = create_user(email='user1@example.com', name='User One')
        if user2 is None:
            user2 = create_user(email='user2@example.com', name='User Two')
        return Friendship.objects.create(user1=user1, user2=user2)
    return _create_friendship

@pytest.fixture
def create_friend_request(create_user):
    def _create_friend_request(sender=None, receiver=None, status=FriendRequest.Status.PENDING):
        if sender is None:
            sender = create_user(email='sender@example.com', name='Sender User')
        if receiver is None:
            receiver = create_user(email='receiver@example.com', name='Receiver User')
        return FriendRequest.objects.create(sender=sender, receiver=receiver, status=status)
    return _create_friend_request


@pytest.mark.django_db
class TestFriendRequests:
    
    def test_send_friend_request_successful(self, api_client, create_user):
        """Test that a user can send a friend request."""
        sender = create_user(email='sender@example.com', name='Sender User')
        receiver = create_user(email='receiver@example.com', name='Receiver User')
        
        api_client.force_authenticate(user=sender)
        url = reverse('send-friend-request', kwargs={'user_id': receiver.id})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert FriendRequest.objects.filter(sender=sender, receiver=receiver).exists()
    
    def test_send_friend_request_to_self_fails(self, api_client, create_user):
        """Test that a user cannot send a friend request to themselves."""
        user = create_user()
        
        api_client.force_authenticate(user=user)
        url = reverse('send-friend-request', kwargs={'user_id': user.id})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not FriendRequest.objects.filter(sender=user, receiver=user).exists()
    
    def test_send_duplicate_friend_request_fails(self, api_client, create_user, create_friend_request):
        """Test that a user cannot send duplicate friend requests."""
        sender = create_user(email='sender@example.com', name='Sender User')
        receiver = create_user(email='receiver@example.com', name='Receiver User')
        
        # Create existing request
        existing_request = create_friend_request(sender=sender, receiver=receiver)
        
        api_client.force_authenticate(user=sender)
        url = reverse('send-friend-request', kwargs={'user_id': receiver.id})
        
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # There should still be only one request
        assert FriendRequest.objects.filter(sender=sender, receiver=receiver).count() == 1
    
    def test_accept_friend_request(self, api_client, create_user, create_friend_request):
        """Test that a user can accept a friend request."""
        sender = create_user(email='sender@example.com', name='Sender User')
        receiver = create_user(email='receiver@example.com', name='Receiver User')
        
        # Create pending request
        friend_request = create_friend_request(sender=sender, receiver=receiver)
        
        api_client.force_authenticate(user=receiver)
        url = reverse('accept-friend-request', kwargs={'request_id': friend_request.id})
        
        response = api_client.put(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the request status was updated
        friend_request.refresh_from_db()
        assert friend_request.status == FriendRequest.Status.ACCEPTED
        
        # Check that a friendship was created
        assert Friendship.objects.filter(
            (Q(user1=sender) & Q(user2=receiver)) | 
            (Q(user1=receiver) & Q(user2=sender))
        ).exists()
    
    def test_reject_friend_request(self, api_client, create_user, create_friend_request):
        """Test that a user can reject a friend request."""
        sender = create_user(email='sender@example.com', name='Sender User')
        receiver = create_user(email='receiver@example.com', name='Receiver User')
        
        # Create pending request
        friend_request = create_friend_request(sender=sender, receiver=receiver)
        
        api_client.force_authenticate(user=receiver)
        url = reverse('reject-friend-request', kwargs={'request_id': friend_request.id})
        
        response = api_client.put(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check that the request status was updated
        friend_request.refresh_from_db()
        assert friend_request.status == FriendRequest.Status.REJECTED
        
        # Check that no friendship was created
        assert not Friendship.objects.filter(
            (Q(user1=sender) & Q(user2=receiver)) | 
            (Q(user1=receiver) & Q(user2=sender))
        ).exists()


@pytest.mark.django_db
class TestFriendList:
    
    def test_list_friends(self, api_client, create_user, create_friendship):
        """Test that a user can list their friends."""
        user1 = create_user(email='user1@example.com', name='User One')
        user2 = create_user(email='user2@example.com', name='User Two')
        user3 = create_user(email='user3@example.com', name='User Three')
        
        # Create friendships
        create_friendship(user1=user1, user2=user2)
        create_friendship(user1=user1, user2=user3)
        
        api_client.force_authenticate(user=user1)
        url = reverse('friend-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        
        # Check the friend IDs in the response
        friend_ids = [friend['friend']['id'] for friend in response.data['results']]
        assert user2.id in friend_ids
        assert user3.id in friend_ids


@pytest.mark.django_db
class TestFriendSuggestions:
    
    def test_get_friend_suggestions(self, api_client, create_user, create_friendship, create_friend_request):
        """Test that a user can get friend suggestions."""
        user1 = create_user(email='user1@example.com', name='User One')
        
        # Create users who are already friends - should not be suggested
        friend1 = create_user(email='friend1@example.com', name='Friend One')
        create_friendship(user1=user1, user2=friend1)
        
        # Create users with pending requests - should not be suggested
        pending_user1 = create_user(email='pending1@example.com', name='Pending One')
        create_friend_request(sender=user1, receiver=pending_user1)
        
        pending_user2 = create_user(email='pending2@example.com', name='Pending Two')
        create_friend_request(sender=pending_user2, receiver=user1)
        
        # Create potential suggestions
        for i in range(10):
            create_user(email=f'suggestion{i}@example.com', name=f'Suggestion User {i}')
        
        api_client.force_authenticate(user=user1)
        url = reverse('friend-suggestions')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Should suggest at most 5 users
        assert len(response.data['results']) <= 5
        
        # Check that friends and pending requests are not suggested
        suggestion_ids = [user['id'] for user in response.data['results']]
        assert friend1.id not in suggestion_ids
        assert pending_user1.id not in suggestion_ids
        assert pending_user2.id not in suggestion_ids
        assert user1.id not in suggestion_ids  # Self should not be suggested