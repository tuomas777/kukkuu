from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.utils.translation import ugettext_lazy as _
from subscriptions.consts import NotificationType

from children.models import Child
from events.models import Occurrence
from events.utils import send_event_notifications_to_guardians
from kukkuu.consts import OCCURRENCE_IS_NOT_FULL_ERROR


class FreeSpotNotificationSubscriptionQueryset(models.QuerySet):
    def user_can_view(self, user):
        return self.filter(
            Q(child__guardians__user=user)
            | Q(child__project__in=user.administered_projects)
        ).distinct()

    def send_notification(self):
        for subscription in self.select_related("occurrence__event"):
            child = subscription.child
            occurrence = subscription.occurrence

            subscription.delete()

            send_event_notifications_to_guardians(
                subscription.occurrence.event,
                NotificationType.FREE_SPOT,
                child,
                occurrence=occurrence,
                subscription=subscription,
            )


class FreeSpotNotificationSubscription(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    child = models.ForeignKey(
        Child,
        verbose_name=_("child"),
        related_name="free_spot_notification_subscriptions",
        on_delete=models.CASCADE,
    )
    occurrence = models.ForeignKey(
        Occurrence,
        verbose_name=_("occurrence"),
        related_name="free_spot_notification_subscriptions",
        on_delete=models.CASCADE,
    )

    objects = FreeSpotNotificationSubscriptionQueryset.as_manager()

    class Meta:
        verbose_name = _("free spot notification subscription")
        verbose_name_plural = _("free spot notification subscriptions")
        ordering = ("id",)
        constraints = (
            UniqueConstraint(
                fields=["child", "occurrence"], name="unique_free_spot_child_occurrence"
            ),
        )

    def __str__(self):
        return f"{self.child} {self.occurrence} subscription"

    def clean(self):
        if not self.pk and self.occurrence.get_remaining_capacity():
            raise ValidationError(
                "Cannot create a free spot subscription for an occurrence that still "
                "has free spots.",
                code=OCCURRENCE_IS_NOT_FULL_ERROR,
            )
