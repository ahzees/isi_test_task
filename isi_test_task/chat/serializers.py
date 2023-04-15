from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "pk",
            "participants",
            "created",
            "updated",
        ]

    def get_participants(self, obj):
        return [user.username for user in obj.participants.all()]


class TheThreadSerializer(ThreadSerializer):
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ["pk", "participants", "created", "updated", "messages_count"]

    def get_messages_count(self, obj):
        return obj.messages.all().count()


class UserThreadSerializer(serializers.ModelSerializer):
    threads = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "pk",
            "threads",
        ]

    def get_threads(self, obj):
        return [threads.pk for threads in obj.threads.all()]


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "sender",
            "thread",
            "text",
        ]


class ThreadMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "pk",
            "sender",
            "text",
            "created",
            "is_read",
        ]


class ViewMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["sender", "thread", "text", "is_read"]
