from django_ilmoitin.utils import send_notification

from events.notifications import NotificationType


def send_event_notifications_to_guardians(
    event, notification_type, guardians, **kwargs
):
    for guardian in guardians:
        if notification_type == NotificationType.EVENT_PUBLISHED:
            context = {"event": event, "guardian": guardian}
            send_notification(
                guardian.user.email,
                notification_type,
                context=context,
                language=guardian.language,
            )
        if notification_type in (
            NotificationType.OCCURRENCE_ENROLMENT,
            NotificationType.OCCURRENCE_UNENROLMENT,
        ):
            context = {
                "guardian": guardian,
                "child": kwargs.get("child"),
                "occurrence": kwargs.get("occurrence"),
            }
            send_notification(
                guardian.user.email,
                notification_type,
                context=context,
                language=guardian.language,
            )
