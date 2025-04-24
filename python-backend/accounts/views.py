from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q
from rest_framework import generics, permissions, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests

from .serializers import (
    UserSerializer,
    UserListSerializer,
    RegisterSerializer,
    GoogleAuthSerializer,
    LoginSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """API view for user registration."""
    
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate token for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """API view for user login with email and password."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate token for the authenticated user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class GoogleAuthView(APIView):
    """API view for Google authentication."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token_id = serializer.validated_data['token_id']
        
        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token_id, 
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            # Extract user information from the verified token
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            profile_picture = idinfo.get('picture', '')
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
                # Update Google-specific fields if needed
                user.is_google_user = True
                user.google_id = google_id
                if not user.name and name:
                    user.name = name
                if not user.profile_picture and profile_picture:
                    user.profile_picture = profile_picture
                user.save()
            except User.DoesNotExist:
                # Create a new user
                user = User.objects.create_user(
                    email=email,
                    name=name,
                    is_google_user=True,
                    google_id=google_id,
                    profile_picture=profile_picture
                )
            
            # Generate token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
            
        except ValueError:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API view for retrieving and updating user profile."""
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """API view for listing users, excluding the authenticated user."""
    
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']
    
    def get_queryset(self):
        # Exclude the authenticated user from the list
        return User.objects.exclude(id=self.request.user.id)