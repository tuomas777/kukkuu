from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext_lazy
from django_ilmoitin.admin import NotificationTemplateAdmin
from django_ilmoitin.models import NotificationTemplate

from .notification_importer import NotificationImporter, NotificationImporterException


class NotificationTemplateAdminWithImporter(NotificationTemplateAdmin):
    list_display = ("type", "get_sync_status")
    actions = ("update_selected",)
    ordering = ("type",)
    change_list_template = "notification_change_list.html"
    importer = None

    def changelist_view(self, request, *args, **kwargs):
        importer = NotificationImporter()
        try:
            importer.fetch_data()
            self.importer = importer
        except NotificationImporterException as e:
            self.message_user(request, e, messages.ERROR)
        return super().changelist_view(request, *args, **kwargs)

    def get_sync_status(self, obj):
        return self.importer.is_notification_in_sync(obj) if self.importer else None

    get_sync_status.short_description = _("in sync with the spreadsheet")
    get_sync_status.boolean = True

    def update_selected(self, request, queryset):
        if self.importer:
            num_of_updated = self.importer.update_notifications(queryset)

            if num_of_updated:
                message = ngettext_lazy(
                    f"Imported {num_of_updated} notification.",
                    f"Imported {num_of_updated} notifications.",
                    num_of_updated,
                )
            else:
                message = _("The notifications were in sync already.")
            self.message_user(request, message, messages.SUCCESS)

    update_selected.short_description = _(
        "Import selected notifications from the spreadsheet"
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "import-new-notifications/",
                self.admin_site.admin_view(self.import_new_notifications),
                name="import-new-notifications",
            ),
        ]
        return custom_urls + urls

    def import_new_notifications(self, request):
        if self.importer:
            num_of_created = self.importer.create_non_existing_notifications()
            if num_of_created:
                message = ngettext_lazy(
                    f"Imported {num_of_created} new notification.",
                    f"Imported {num_of_created} new notifications.",
                    num_of_created,
                )
            else:
                message = _("No new notifications.")
            self.message_user(request, message, messages.SUCCESS)
        return HttpResponseRedirect(
            reverse("admin:django_ilmoitin_notificationtemplate_changelist")
        )


if settings.KUKKUU_NOTIFICATIONS_SHEET_ID:
    admin.site.unregister(NotificationTemplate)
    admin.site.register(NotificationTemplate, NotificationTemplateAdminWithImporter)
