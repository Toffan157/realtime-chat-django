from rest_framework import serializers
from .models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'room', 'username', 'content', 'image', 'content_type', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'room']
