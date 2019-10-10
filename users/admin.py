from django.contrib import admin
from django.contrib.auth import get_user_model

from children.models import Relationship


class RelationshipInline(admin.TabularInline):
    model = Relationship
    extra = 0
    fields = ("child", "type", "created_at")
    readonly_fields = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    inlines = (RelationshipInline,)
