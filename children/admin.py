from django.contrib import admin

from events.models import Enrolment

from .models import Child, Relationship


class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 0
    fields = ("guardian", "type", "created_at")
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


class EnrolmentInline(admin.TabularInline):
    model = Enrolment
    extra = 1
    readonly_fields = ("created_at",)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "birthdate",
        "postal_code",
        "created_at",
        "updated_at",
    )
    fields = ("first_name", "last_name", "birthdate", "postal_code")
    inlines = (RelationshipInline, EnrolmentInline)
