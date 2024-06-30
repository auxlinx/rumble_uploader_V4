"""
Module-level docstring describing the purpose of the module.
"""

from rest_framework import serializers
from .models import RumbleVideo, YouTubeVideo

class RumbleVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RumbleVideo
        fields = '__all__'  # This will include all fields in the serializer

class YouTubeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeVideo
        fields = '__all__'  # This will include all fields in the serializer
