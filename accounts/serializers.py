from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "is_craftsman", "photo", "phone", "governorate", "city")