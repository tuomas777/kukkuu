from django.core.management import BaseCommand

from common.notification_sync import NotificationSyncher


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f"Synching notifications from the spreadsheet...")

        syncher = NotificationSyncher()
        (
            num_of_created,
            num_of_updated,
        ) = syncher.create_non_existing_and_update_existing_notifications()

        self.stdout.write(
            self.style.SUCCESS(
                f"Great success! Created {num_of_created} new notification(s) and "
                f"updated {num_of_updated} already existing notification(s)."
            )
        )
