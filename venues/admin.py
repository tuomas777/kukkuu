from django.contrib import admin

from venues.models import Venue


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "seat_count", "created_at", "updated_at")
    list_display_links = ("id", "name")
    fields = ("name", "description", "seat_count")
