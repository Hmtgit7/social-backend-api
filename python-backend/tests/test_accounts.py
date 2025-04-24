import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

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

@pytest.mark.django_db
class TestUserRegistration:
    
    def test_user_registration_successful(self, api_client):
        """Test that a user can register successfully."""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'StrongP@ss123',
            'password_confirm': 'StrongP@ss123',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
        assert User.objects.filter(email='newuser@example.com').exists()
    
    def test_user_registration_password_mismatch(self, api_client):
        """Test that registration fails when passwords don't match."""
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'name': 'New User',
            'password': 'StrongP@ss123',
            'password_confirm': 'DifferentP@ss',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data
        assert not User.objects.filter(email='newuser@example.com').exists()


@pytest.mark.django_db
class TestUserLogin:
    
    def test_user_login_successful(self, api_client, create_user):
        """Test that a user can login successfully."""
        user = create_user()
        url = reverse('login')
        data = {
            'email': 'user@example.com',
            'password': 'password123',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert 'user' in response.data
    
    def test_user_login_invalid_credentials(self, api_client, create_user):
        """Test that login fails with invalid credentials."""
        user = create_user()
        url = reverse('login')
        data = {
            'email': 'user@example.com',
            'password': 'wrongpassword',
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfile:
    
    def test_get_user_profile(self, api_client, create_user):
        """Test that an authenticated user can get their profile."""
        user = create_user()
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['name'] == user.name
    
    def test_update_user_profile(self, api_client, create_user):
        """Test that an authenticated user can update their profile."""
        user = create_user()
        api_client.force_authenticate(user=user)
        url = reverse('user-profile')
        data = {
            'name': 'Updated Name',
            'bio': 'This is my new bio'
        }
        
        response = api_client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Name'
        assert response.data['bio'] == 'This is my new bio'
        
        # Refresh user from database
        user.refresh_from_db()
        assert user.name == 'Updated Name'
        assert user.bio == 'This is my new bio'


@pytest.mark.django_db
class TestUserList:
    
    def test_list_users_excludes_self(self, api_client, create_user):
        """Test that the user list endpoint excludes the authenticated user."""
        user1 = create_user(email='user1@example.com', name='User One')
        user2 = create_user(email='user2@example.com', name='User Two')
        user3 = create_user(email='user3@example.com', name='User Three')
        
        api_client.force_authenticate(user=user1)
        url = reverse('user-list')
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  # Exclude self
        
        # Check that user1 (self) is not in the results
        user_emails = [user['email'] for user in response.data['results']]
        assert 'user1@example.com' not in user_emails
        assert 'user2@example.com' in user_emails
        assert 'user3@example.com' in user_emails
    
    def test_search_users_by_name(self, api_client, create_user):
        """Test that users can be searched by name."""
        user1 = create_user(email='user1@example.com', name='John Doe')
        user2 = create_user(email='user2@example.com', name='Jane Smith')
        user3 = create_user(email='user3@example.com', name='John Smith')
        
        api_client.force_authenticate(user=user1)
        url = reverse('user-list') + '?search=Smith'
        
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2  # Both users with 'Smith'
        
        # Check that only 'Smith' users are in the results
        user_names = [user['name'] for user in response.data['results']]
        assert 'John Doe' not in user_names
        assert 'Jane Smith' in user_names
        assert 'John Smith' in user_names