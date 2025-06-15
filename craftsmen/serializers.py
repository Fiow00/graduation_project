from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Craftsman, Comment

class CraftsmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Craftsman
        fields = ("user", "photo", "service", "bio", "governorate", "city", "experience_years", "certifications")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Show author's username
    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'created_at')