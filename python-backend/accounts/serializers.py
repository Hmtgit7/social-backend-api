from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'bio', 'profile_picture']
        read_only_fields = ['id', 'email']


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'profile_picture']
        read_only_fields = ['id', 'email', 'name', 'profile_picture']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        """Validate that passwords match and meet requirements."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Password fields didn't match."})
        
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs
    
    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class GoogleAuthSerializer(serializers.Serializer):
    """Serializer for Google authentication."""
    
    token_id = serializers.CharField(required=True)
    
    def validate_token_id(self, value):
        """Validate Google token ID."""
        # Token validation logic would go here in a real implementation
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})