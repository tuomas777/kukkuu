from random import random

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatedFields
from projects.models import Project

from common.models import TimestampedModel, TranslatableModel, TranslatableQuerySet
from events.models import Event, Occurrence
from users.models import Guardian


class MessageQuerySet(TranslatableQuerySet):
    def user_can_view(self, user):
        return self.filter(project__users=user)


class Message(TimestampedModel, TranslatableModel):
    ALL = "all"
    INVITED = "invited"
    ENROLLED = "enrolled"
    ATTENDED = "attended"
    SUBSCRIBED_TO_FREE_SPOT_NOTIFICATION = "subscribed_to_free_spot_notification"
    RECIPIENT_SELECTION_CHOICES = (
        (ALL, _("All")),
        (INVITED, _("Invited")),
        (ENROLLED, _("Enrolled")),
        (ATTENDED, _("Attended")),
        (
            SUBSCRIBED_TO_FREE_SPOT_NOTIFICATION,
            _("Subscribed to free spot notification"),
        ),
    )

    project = models.ForeignKey(
        Project,
        verbose_name=_("project"),
        related_name="messages",
        on_delete=models.CASCADE,
    )
    translations = TranslatedFields(
        subject=models.CharField(verbose_name=_("subject"), max_length=255),
        body_text=models.TextField(verbose_name=_("body plain text")),
    )
    sent_at = models.DateTimeField(verbose_name=_("sent at"), blank=True, null=True)
    recipient_count = models.PositiveIntegerField(
        verbose_name=_("recipient count"), blank=True, null=True
    )
    recipient_selection = models.CharField(
        max_length=64,
        verbose_name=_("recipient selection"),
        choices=RECIPIENT_SELECTION_CHOICES,
    )
    event = models.ForeignKey(
        Event,
        verbose_name=_("event"),
        related_name="messages",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    occurrences = models.ManyToManyField(
        Occurrence, verbose_name=_("occurrences"), related_name="messages", blank=True,
    )

    objects = MessageQuerySet.as_manager()

    class Meta:
        ordering = ("id",)
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return f"({self.pk}) {self.subject} ({self.sent_at or 'not sent'})"

    def send(self):
        self.recipient_count = (
            Guardian.objects.filter(children__project=self.project).count()
            if self.recipient_selection == Message.ALL
            else random.randint(
                0, 50
            )  # TODO temporary thingy before actual send implementation
        )
        self.sent_at = now()
        self.save(update_fields=("recipient_count", "sent_at"))

    def can_user_administer(self, user):
        return user.projects.filter(pk=self.project.pk).exists()
