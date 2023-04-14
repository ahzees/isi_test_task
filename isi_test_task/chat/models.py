from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_participants(elem):
    if elem.count() > 2:
        raise ValidationError("Thread can't have more than 2 participants.")


# Create your models here.
class Thread(models.Model):
    participants = models.ForeignKey(
        User,
        related_name="threads",
        validators=[validate_participants],
        verbose_name="participants",
        on_delete=models.DO_NOTHING,
    )
    created = models.DateTimeField("Created at", auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk}"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="messages",
        on_delete=models.DO_NOTHING,
        verbose_name="Sender",
    )
    text = models.TextField("Text")
    thread = models.ForeignKey(
        Thread, related_name="messages", on_delete=models.DO_NOTHING
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.pk}"
