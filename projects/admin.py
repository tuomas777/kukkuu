from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from parler.admin import TranslatableAdmin
from projects.models import Project


class ProjectInline(admin.TabularInline):
    model = Project.users.through
    extra = 0


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin, GuardedModelAdmin):
    change_form_template = "change_form.html"
    list_display = ("id", "year", "name")
    list_display_links = ("id", "year")
    fields = ("year", "name", "users")
    inlines = (ProjectInline,)
