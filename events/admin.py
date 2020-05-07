from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from .models import Event, Occurrence


class OccurrencesInline(admin.StackedInline):
    model = Occurrence
    extra = 1


@admin.register(Event)
class EventAdmin(TranslatableAdmin):
    list_display = (
        "id",
        "name",
        "short_description",
        "capacity_per_occurrence",
        "participants_per_invite",
        "is_published",
    )
    list_display_links = ("id", "name")
    exclude = ("id", "created_at", "updated_at", "published_at")
    inlines = [
        OccurrencesInline,
    ]
    actions = ["publish"]

    def publish(self, request, queryset):
        for obj in queryset:
            obj.publish()
        self.message_user(request, _("%s successfully published.") % queryset.count())

    publish.short_description = _("Publish selected events")


@admin.register(Occurrence)
class OccurrenceAdmin(admin.ModelAdmin):
    list_display = ("id", "time", "event", "created_at", "updated_at")
    list_display_links = ("id", "time")
    fields = ("time", "event", "venue")
