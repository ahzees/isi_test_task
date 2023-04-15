from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver

from .models import Message, Thread


# створення сигналу, який не буде дозволяти створювати тред, для більш ніж 2-х користувачів
@receiver(m2m_changed, sender=Thread.participants.through)
def validate_thread_participants(sender, instance, action, **kwargs):
    if action == "pre_add":
        num_participants = instance.participants.count() + len(kwargs["pk_set"])
        if num_participants > 2:
            raise ValidationError("Thread can't have more than 2 participants.")


# створення сигналу, який буде перевіряти, чи надсилач повідомлення є учасником треду
@receiver(pre_save, sender=Message)
def validate_message_sender(sender, instance, **kwargs):
    if not instance.sender.pk in [
        i[0] for i in instance.thread.participants.values_list("pk")
    ]:
        raise ValidationError(
            f"Message can only be sent by a member of the thread ({instance.sender.pk} is not a member)."
        )
