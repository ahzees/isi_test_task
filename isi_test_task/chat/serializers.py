from rest_framework import serializers

from .models import *


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "participants",
        ]

    def get_participants(self, obj):
        return [user.username for user in obj.participants.all()]
