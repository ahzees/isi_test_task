from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver

from .models import Message, Thread


@receiver(m2m_changed, sender=Thread.participants.through)
def validate_thread_participants(sender, instance, action, **kwargs):
    if action == "pre_add":
        num_participants = instance.participants.count() + len(kwargs["pk_set"])
        if num_participants > 2:
            raise ValidationError("Thread can't have more than 2 participants.")


@receiver(pre_save, sender=Message)
def validate_message_sender(sender, instance, **kwargs):
    if not instance.sender.pk in [
        i[0] for i in instance.thread.participants.values_list("pk")
    ]:
        raise ValidationError("Message can be send only from member of thread")
