from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Thread(models.Model):
    participants = models.ManyToManyField(
        User,
        related_name="threads",
        verbose_name="participants",
    )
    created = models.DateTimeField("Created at", auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)

    def __str__(self) -> str:
        return f"{self.pk}"


class Message(models.Model):
    sender = models.ManyToManyField(
        User,
        related_name="messages",
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
