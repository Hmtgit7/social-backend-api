from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class FriendRequest(models.Model):
    """Model for friend requests between users."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('sender', 'receiver')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"
    
    @property
    def is_active(self):
        """Check if the request is still active (pending)."""
        return self.status == self.Status.PENDING


class Friendship(models.Model):
    """Model for established friendships between users."""
    
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships1'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user1} & {self.user2}"