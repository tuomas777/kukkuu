from django.contrib import admin
from parler.admin import TranslatableAdmin
from projects.models import Project


class ProjectInline(admin.TabularInline):
    model = Project.users.through
    extra = 0


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ("id", "year", "name")
    list_display_links = ("id", "year")
    fields = ("year", "name", "users")
    inlines = (ProjectInline,)
