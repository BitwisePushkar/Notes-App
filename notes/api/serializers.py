from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Info
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=8,error_messages={
        'min_length': 'Password must be at least 8 characters long.',})
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True},'email': {'required': True}}

    def validate_username(self, value):
        if len(value) < 3 or len(value) > 20:
            raise serializers.ValidationError("Username must be between 3 and 20 characters.")
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', value):
            raise serializers.ValidationError("Username must start with a letter and contain only letters, numbers, and underscores.")
        return value

    def validate_password(self, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Password must be at least 8 characters long, include uppercase, lowercase, digit, and special character.")
        return value

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Enter a valid email address.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        return value

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'],
                                        password=validated_data['password'])
        return user

class InfoSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Info
        fields = ['id', 'title', 'text', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value.strip()
    
    def validate_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Text cannot be empty.")
        return value.strip()