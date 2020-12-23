from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from parler.admin import TranslatableAdmin
from projects.models import Project


@admin.register(Project)
class ProjectAdmin(TranslatableAdmin, GuardedModelAdmin):
    change_form_template = "project_change_form.html"
    list_display = ("year", "name")
    fields = ("year", "name")
