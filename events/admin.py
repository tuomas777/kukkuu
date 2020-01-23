from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Event, Occurrence


@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "name",
        "short_description",
        "capacity_per_occurrence",
        "participants_per_invite",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    exclude = ("id", "created_at", "updated_at")


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "event", "created_at", "updated_at")
    list_display_links = ("id", "time")
    fields = ("time", "event", "venue")
