from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    craftsmen_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Service
        fields = ['id', 'title', 'image', 'slug', 'craftsmen_count']
    
    def get_craftmen_count(self, obj):
        return obj.craftsmen.filter(is_verified=True).count()