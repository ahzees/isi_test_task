from rest_framework import serializers

from .models import *


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = [
            "participants",
        ]
