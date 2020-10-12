from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Message


@admin.register(Message)
class MessageAdmin(TranslatableAdmin):
    list_display = (
        "subject",
        "project",
        "sent_at",
        "recipient_count",
        "created_at",
        "updated_at",
    )
    fields = (
        "project",
        "subject",
        "body_text",
        "recipient_selection",
        "event",
        "occurrences",
        "created_at",
        "updated_at",
        "recipient_count",
    )
    readonly_fields = ("recipient_count", "created_at", "updated_at")
