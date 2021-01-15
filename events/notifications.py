from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications
from projects.factories import ProjectFactory

from children.factories import ChildWithGuardianFactory
from common.utils import get_global_id
from events.consts import NotificationType
from events.factories import (
    EnrolmentFactory,
    EventFactory,
    EventGroupFactory,
    OccurrenceFactory,
)
from events.utils import get_event_ui_url, get_occurrence_ui_url
from users.factories import GuardianFactory
from venues.factories import VenueFactory

notifications.register(NotificationType.EVENT_PUBLISHED, _("event published"))
notifications.register(
    NotificationType.EVENT_GROUP_PUBLISHED, _("event group published")
)
notifications.register(NotificationType.OCCURRENCE_ENROLMENT, _("occurrence enrolment"))
notifications.register(
    NotificationType.OCCURRENCE_UNENROLMENT, _("occurrence unenrolment")
)
notifications.register(NotificationType.OCCURRENCE_CANCELLED, _("occurrence cancelled"))
notifications.register(NotificationType.OCCURRENCE_REMINDER, _("occurrence reminder"))

project = ProjectFactory.build(year=2020)
event = EventFactory.build(project=project)
event_group = EventGroupFactory.build(project=project)
event_with_event_group = EventFactory.build(project=project, event_group=event_group)
venue = VenueFactory.build(project=project)
guardian = GuardianFactory.build()
child = ChildWithGuardianFactory.build(relationship__guardian=guardian, project=project)
occurrence = OccurrenceFactory.build(event=event, venue=venue)
enrolment = EnrolmentFactory.build(occurrence=occurrence, child=child)

dummy_context.update(
    {
        NotificationType.EVENT_PUBLISHED: {
            "guardian": guardian,
            "event": event,
            "child": child,
            "event_url": get_event_ui_url(event, child, guardian.language),
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
        },
        NotificationType.OCCURRENCE_ENROLMENT: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
        },
        NotificationType.OCCURRENCE_UNENROLMENT: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
        },
        NotificationType.OCCURRENCE_CANCELLED: {
            "guardian": guardian,
            "occurrence": occurrence,
            "child": child,
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
        },
        NotificationType.OCCURRENCE_REMINDER: {
            "guardian": guardian,
            "event": event,
            "occurrence": occurrence,
            "child": child,
            "enrolment": enrolment,
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
            "occurrence_url": get_occurrence_ui_url(
                occurrence, child, guardian.language
            ),
        },
        NotificationType.EVENT_GROUP_PUBLISHED: {
            "guardian": guardian,
            "events": [
                {
                    "obj": event,
                    "occurrence": occurrence,
                    "child": child,
                    "enrolment": enrolment,
                }
            ],
            "localtime": timezone.template_localtime,
            "get_global_id": get_global_id,
        },
    }
)
