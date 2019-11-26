from django.utils.translation import ugettext_lazy as _
from django_ilmoitin.dummy_context import dummy_context
from django_ilmoitin.registry import notifications

from users.factories import GuardianFactory

from .factories import ChildWithGuardianFactory


class NotificationType:
    SIGNUP = "signup"


notifications.register(NotificationType.SIGNUP, _("signup"))


guardian = GuardianFactory.build()
children = ChildWithGuardianFactory.build_batch(3, relationship__guardian=guardian)

dummy_context.update(
    {NotificationType.SIGNUP: {"children": children, "guardian": guardian}}
)
