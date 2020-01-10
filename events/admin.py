from django.contrib import admin

from .models import Event, Occurrence


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "short_description",
        "duration",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    fields = ("name", "short_description", "description", "duration")


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "event", "created_at", "updated_at")
    list_display_links = ("id", "time")
    fields = ("time", "event")
