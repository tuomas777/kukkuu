from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from children.factories import ChildWithGuardianFactory
from events.consts import NotificationType
from events.factories import EnrolmentFactory, EventFactory, OccurrenceFactory
from events.utils import get_event_ui_url
from users.factories import GuardianFactory

notifications.register(NotificationType.EVENT_PUBLISHED, _("event published"))
notifications.register(NotificationType.OCCURRENCE_ENROLMENT, _("occurrence enrolment"))
notifications.register(
    NotificationType.OCCURRENCE_UNENROLMENT, _("occurrence unenrolment")
)
notifications.register(NotificationType.OCCURRENCE_CANCELLED, _("occurrence cancelled"))
notifications.register(NotificationType.OCCURRENCE_REMINDER, _("occurrence reminder"))

event = EventFactory.build()
guardian = GuardianFactory.build()
child = ChildWithGuardianFactory.build(relationship__guardian=guardian)
occurrence = OccurrenceFactory.build(event=event)
enrolment = EnrolmentFactory.build(occurrence=occurrence, child=child)

dummy_context.update(
    {
        NotificationType.EVENT_PUBLISHED: {
            "guardian": guardian,
            "event": event,
            "child": child,
            "event_url": get_event_ui_url(event, child, guardian.language),
        },
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
        NotificationType.OCCURRENCE_CANCELLED: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
        },
        NotificationType.OCCURRENCE_REMINDER: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
            "enrolment": enrolment,
        },
    }
)
