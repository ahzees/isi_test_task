from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Thread


@receiver(m2m_changed, sender=Thread.participants.through)
def validate_thread_participants(sender, instance, action, **kwargs):
    if action == "pre_add":
        num_participants = instance.participants.count() + len(kwargs["pk_set"])
        if num_participants > 2:
            raise ValidationError("Thread can't have more than 2 participants.")
