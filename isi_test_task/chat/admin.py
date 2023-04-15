from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Case, Count, When

from .models import Message, Thread

# Register your models here.


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Participants", {"fields": ("participants",)}),
        ("Important dates", {"fields": ("created", "updated")}),
    )
    inlines = [MessageInline]
    list_display = ("pk", "created", "amount_of_messages", "list_participants")
    list_display_links = ("pk", "created", "amount_of_messages")
    search_fields = ("participants__username", "pk", "created")
    readonly_fields = ("created", "updated")
    ordering = ("updated",)
    sortable_by = ("participants",)

    def list_participants(self, obj):
        return [user.username for user in obj.participants.all()]

    def amount_of_messages(self, obj):
        return obj.messages.all().count()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("pk", "sender", "created", "text", "thread")
    list_display_links = (
        "created",
        "pk",
    )
    search_fields = ("sender__username", "thread__pk", "pk", "text")


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "pk", "is_staff", "is_superuser", "last_login")
    list_display_links = (
        "username",
        "pk",
    )
    search_fields = ("pk", "username")
    readonly_fields = ("last_login", "list_threads", "new_messages")
    fieldsets = (
        (None, {"fields": ("username",)}),
        ("Personal information", {"fields": ("last_login", "list_threads")}),
        ("New Messages", {"fields": ("new_messages",)}),
    )

    def list_threads(self, obj):
        return [str(i) for i in obj.threads.all()]

    def new_messages(self, obj):
        return (
            Message.objects.filter(is_read=False)
            .filter(thread__participants=obj)
            .exclude(sender=obj)
            .count()
        )
