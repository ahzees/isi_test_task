from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class ThreadSerializer(serializers.ModelSerializer):
    # серіалізатор для списка тредів

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
    # серіалізатор для конкретного треду

    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ["pk", "participants", "created", "updated", "messages_count"]

    def get_messages_count(self, obj):
        return obj.messages.all().count()


class UserThreadSerializer(serializers.ModelSerializer):
    # серіалізатор для всіх тредів користувача

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
    # серіалізатор для створення повідомлення в треді

    class Meta:
        model = Message
        fields = [
            "sender",
            "thread",
            "text",
        ]


class ThreadMessagesSerializer(serializers.ModelSerializer):
    # серіалізатор для всіх повідомлень у треді

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
    # серіалізатор для перегляду повідомлень

    class Meta:
        model = Message
        fields = ["sender", "thread", "text", "is_read"]
