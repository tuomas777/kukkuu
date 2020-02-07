from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from children.factories import ChildWithGuardianFactory
from events.factories import EventFactory, OccurrenceFactory
from users.factories import GuardianFactory


class NotificationType:
    EVENT_PUBLISHED = "event_published"
    OCCURRENCE_ENROLMENT = "occurrence_enrolment"
    OCCURRENCE_UNENROLMENT = "occurrence_unenrolment"


notifications.register(NotificationType.EVENT_PUBLISHED, _("event published"))
notifications.register(NotificationType.OCCURRENCE_ENROLMENT, _("occurrence enrolment"))
notifications.register(
    NotificationType.OCCURRENCE_UNENROLMENT, _("occurrence " "unenrolment")
)

event = EventFactory.build()
guardian = GuardianFactory.build()
child = ChildWithGuardianFactory.build(relationship__guardian=guardian)
occurrence = OccurrenceFactory.build(event=event)

dummy_context.update(
    {
        NotificationType.EVENT_PUBLISHED: {"guardian": guardian, "event": event},
        NotificationType.OCCURRENCE_ENROLMENT: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
        },
        NotificationType.OCCURRENCE_UNENROLMENT: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
        },
    }
)
