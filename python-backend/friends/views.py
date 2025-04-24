import random
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from .models import FriendRequest, Friendship
from .serializers import (
    FriendRequestSerializer,
    FriendshipSerializer,
    FriendSuggestionSerializer,
)

User = get_user_model()


class FriendListView(generics.ListAPIView):
    """API view for listing all friends of the authenticated user."""

    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get all friendships where the user is either user1 or user2
        return Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

    def get_serializer_context(self):
        """Add request to serializer context."""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class FriendRequestListView(generics.ListAPIView):
    """API view for listing all friend requests of the authenticated user."""

    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get all friend requests where the user is either sender or receiver
        return FriendRequest.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )


class SendFriendRequestView(APIView):
    """API view for sending a friend request to another user."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        sender = request.user

        try:
            receiver = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if trying to send request to self
        if sender == receiver:
            return Response(
                {"detail": "You cannot send a friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already friends
        friendship_exists = Friendship.objects.filter(
            (Q(user1=sender) & Q(user2=receiver)) |
            (Q(user1=receiver) & Q(user2=sender))
        ).exists()

        if friendship_exists:
            return Response(
                {"detail": "You are already friends with this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if request already exists
        request_exists = FriendRequest.objects.filter(
            sender=sender,
            receiver=receiver
        ).exists()

        if request_exists:
            return Response(
                {"detail": "A friend request has already been sent to this user."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if there's a pending request in the opposite direction
        opposite_request = FriendRequest.objects.filter(
            sender=receiver,
            receiver=sender,
            status=FriendRequest.Status.PENDING
        ).first()

        if opposite_request:
            # Auto-accept the opposite request
            opposite_request.status = FriendRequest.Status.ACCEPTED
            opposite_request.save()

            # Create friendship
            Friendship.objects.create(user1=sender, user2=receiver)

            return Response({
                "detail": "Friend request accepted automatically as they had already requested you.",
                "friend_request": FriendRequestSerializer(opposite_request).data
            }, status=status.HTTP_201_CREATED)

        # Create new friend request
        friend_request = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver
        )

        return Response(
            FriendRequestSerializer(friend_request).data,
            status=status.HTTP_201_CREATED
        )


class RespondToFriendRequestView(APIView):
    """API view for accepting or rejecting a friend request."""

    permission_classes = [permissions.IsAuthenticated]
    action = None  # Add this line

    def put(self, request, request_id, action=None):
        """Handle accepting or rejecting friend requests.

        The 'action' parameter is passed from the URL configuration.
        """
        user = request.user

        try:
            friend_request = FriendRequest.objects.get(
                id=request_id, receiver=user)
        except FriendRequest.DoesNotExist:
            return Response(
                {"detail": "Friend request not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the request is still pending
        if friend_request.status != FriendRequest.Status.PENDING:
            return Response(
                {"detail": f"This friend request has already been {friend_request.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if action == 'accept':
            friend_request.status = FriendRequest.Status.ACCEPTED
            friend_request.save()

            # Create friendship
            Friendship.objects.create(
                user1=friend_request.sender,
                user2=friend_request.receiver
            )

            return Response(
                {"detail": "Friend request accepted successfully."},
                status=status.HTTP_200_OK
            )

        elif action == 'reject':
            friend_request.status = FriendRequest.Status.REJECTED
            friend_request.save()

            return Response(
                {"detail": "Friend request rejected successfully."},
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"detail": "Invalid action. Use 'accept' or 'reject'."},
                status=status.HTTP_400_BAD_REQUEST
            )


class FriendSuggestionView(generics.ListAPIView):
    """API view for suggesting potential friends."""

    serializer_class = FriendSuggestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get IDs of users who are already friends with the current user
        friend_ids = set()
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        for friendship in friendships:
            friend = friendship.user1 if friendship.user2 == user else friendship.user2
            friend_ids.add(friend.id)

        # Get IDs of users who have pending friend requests with the current user
        request_user_ids = set()
        requests = FriendRequest.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
        for req in requests:
            other_user = req.receiver if req.sender == user else req.sender
            request_user_ids.add(other_user.id)

        # Exclude friends, requests, and self from potential suggestions
        excluded_ids = friend_ids.union(request_user_ids)
        excluded_ids.add(user.id)

        # Get potential suggestions
        suggestions = User.objects.exclude(id__in=excluded_ids)

        # Randomly select up to 5 users
        suggestion_count = min(5, suggestions.count())
        if suggestion_count > 0:
            suggestion_ids = random.sample(
                list(suggestions.values_list('id', flat=True)), suggestion_count)
            return User.objects.filter(id__in=suggestion_ids)

        return User.objects.none()
