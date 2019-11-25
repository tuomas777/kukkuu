from django import forms
from django.conf import settings
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


class GuardianForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"] = forms.ChoiceField(choices=settings.LANGUAGES)


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    form = GuardianForm
    inlines = (RelationshipInline,)
