from django.contrib import admin
from parler.admin import TranslatableAdmin
from projects.models import Project


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ("id", "year", "name")
    list_display_links = ("id", "year")
    fields = ("year", "name", "users")
