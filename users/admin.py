from django.contrib import admin

from children.models import Relationship
from users.models import Guardian


class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 0
    fields = ("child", "type", "created_at")
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    inlines = (RelationshipInline,)
