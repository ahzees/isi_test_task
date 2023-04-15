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

    class Meta:
        verbose_name_plural = "Threads"

    def __str__(self) -> str:
        return f"Thread ID: {self.pk}"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name="messages",
        verbose_name="sender",
        null=True,
    )
    text = models.TextField("Text")
    thread = models.ForeignKey(
        Thread, related_name="messages", on_delete=models.DO_NOTHING
    )
    created = models.DateTimeField("Created at", auto_now_add=True)
    is_read = models.BooleanField("Is read", default=False)

    class Meta:
        verbose_name_plural = "Messages"

    def __str__(self) -> str:
        return f"{self.pk}"
