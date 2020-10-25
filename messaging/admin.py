from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from .models import AlreadySentError, Message


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
    actions = ("send",)

    def send(self, request, queryset):
        sent_count = 0
        for obj in queryset:
            try:
                obj.send()
                sent_count += 1
            except AlreadySentError:
                pass
        self.message_user(request, _("%s successfully sent.") % sent_count)
