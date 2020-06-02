from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatedFields

from children.models import Child
from common.models import TimestampedModel, TranslatableModel, TranslatableQuerySet
from events.consts import NotificationType
from events.utils import send_event_notifications_to_guardians
from venues.models import Venue


# This need to be inherited from TranslatableQuerySet instead of default model.QuerySet
class EventQueryset(TranslatableQuerySet):
    def user_can_view(self, user):
        return self.filter(
            Q(project__users=user) | Q(published_at__isnull=False)
        ).distinct()


class Event(TimestampedModel, TranslatableModel):
    CHILD_AND_GUARDIAN = "child_and_guardian"
    FAMILY = "family"
    PARTICIPANT_AMOUNT_CHOICES = (
        (CHILD_AND_GUARDIAN, _("Child and Guardian")),
        (FAMILY, _("Family")),
    )

    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("name"), max_length=255, blank=True),
        short_description=models.TextField(
            verbose_name=_("short description"), blank=True
        ),
        description=models.TextField(verbose_name=_("description"), blank=True),
        image_alt_text=models.CharField(
            verbose_name=_("image alt text"), blank=True, max_length=255
        ),
    )
    image = models.ImageField(blank=True, verbose_name=_("image"))
    participants_per_invite = models.CharField(
        max_length=255,
        choices=PARTICIPANT_AMOUNT_CHOICES,
        verbose_name=_("participants per invite"),
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name=_("duration"), blank=True, null=True, help_text=_("In minutes")
    )
    capacity_per_occurrence = models.PositiveSmallIntegerField(
        verbose_name=_("capacity per occurrence")
    )
    published_at = models.DateTimeField(
        blank=True, null=True, verbose_name=_("published at")
    )

    project = models.ForeignKey(
        "projects.Project",
        verbose_name=_("project"),
        related_name="events",
        on_delete=models.CASCADE,
    )

    objects = EventQueryset.as_manager()

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return self.safe_translation_getter("name", super().__str__())

    def publish(self):
        self.published_at = timezone.now()
        self.save()

        send_event_notifications_to_guardians(
            self,
            NotificationType.EVENT_PUBLISHED,
            self.project.children.prefetch_related("guardians"),
        )

    def is_published(self):
        return bool(self.published_at)


class OccurrenceQueryset(models.QuerySet):
    def user_can_view(self, user):
        return self.filter(
            Q(event__project__users=user) | Q(event__published_at__isnull=False)
        ).distinct()


class Occurrence(TimestampedModel):
    time = models.DateTimeField(verbose_name=_("time"))
    event = models.ForeignKey(
        Event,
        verbose_name=_("event"),
        related_name="occurrences",
        on_delete=models.CASCADE,
    )
    venue = models.ForeignKey(
        Venue,
        verbose_name=_("venue"),
        related_name="occurrences",
        on_delete=models.CASCADE,
    )

    children = models.ManyToManyField(
        Child,
        verbose_name=_("children"),
        related_name="occurrences",
        through="events.Enrolment",
        blank=True,
    )
    occurrence_language = models.CharField(
        max_length=10,
        choices=settings.LANGUAGES,
        verbose_name=_("occurrence language"),
        default=settings.LANGUAGES[0][0],
    )
    objects = OccurrenceQueryset.as_manager()

    class Meta:
        verbose_name = _("occurrence")
        verbose_name_plural = _("occurrences")

    def __str__(self):
        return f"{self.pk} {self.time}"


class Enrolment(models.Model):
    child = models.ForeignKey(
        Child,
        related_name="enrolments",
        on_delete=models.CASCADE,
        verbose_name=_("child"),
    )
    occurrence = models.ForeignKey(
        Occurrence,
        related_name="enrolments",
        on_delete=models.CASCADE,
        verbose_name=_("occurrence"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        verbose_name = _("enrolment")
        verbose_name_plural = _("enrolments")
        constraints = [
            models.UniqueConstraint(
                fields=["child", "occurrence"], name="unq_child_occurrence"
            )
        ]

    def __str__(self):
        return f"{self.pk} {self.child_id}"
