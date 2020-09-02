from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Language


@admin.register(Language)
class LanguageAdmin(TranslatableAdmin):
    list_display = ("alpha_3_code", "name")
