from django_ilmoitin.utils import send_notification

from users.notifications import NotificationType


def send_guardian_email_changed_notification(guardian):
    send_notification(
        guardian.email,
        NotificationType.GUARDIAN_EMAIL_CHANGED,
        context={"guardian": guardian},
        language=guardian.language,
    )
