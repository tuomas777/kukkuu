from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from events.factories import EventFactory
from users.factories import GuardianFactory


class NotificationType:
    EVENT_PUBLISHED = "event_published"


notifications.register(NotificationType.EVENT_PUBLISHED, _("event published"))

event = EventFactory.build()
guardian = GuardianFactory.build()

dummy_context.update(
    {NotificationType.EVENT_PUBLISHED: {"guardian": guardian, "event": event}}
)
