from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import TimestampedModel, UUIDPrimaryKeyModel
from users.models import Guardian


class ChildQuerySet(models.QuerySet):
    def user_can_view(self, user):
        # TODO we'll probably need more fine-grained control than this
        if user.is_staff:
            return self
        else:
            return self.filter(guardians__user=user)

    def user_can_update(self, user):
        return self.filter(guardians__user=user)

    def user_can_delete(self, user):
        return self.filter(guardians__user=user)


postal_code_validator = RegexValidator(
    regex=r"^\d{5}$", message="Postal code must be 5 digits", code="invalid_postal_code"
)


class Child(UUIDPrimaryKeyModel, TimestampedModel):
    first_name = models.CharField(
        verbose_name=_("first name"), max_length=64, blank=True
    )
    last_name = models.CharField(verbose_name=_("last name"), max_length=64, blank=True)
    birthdate = models.DateField(verbose_name=_("birthdate"))
    postal_code = models.CharField(
        verbose_name=_("postal code"),
        max_length=5,
        blank=True,
        validators=[postal_code_validator],
    )
    guardians = models.ManyToManyField(
        Guardian,
        verbose_name=_("guardians"),
        related_name="children",
        through="children.Relationship",
        blank=True,
    )

    objects = ChildQuerySet.as_manager()

    class Meta:
        verbose_name = _("child")
        verbose_name_plural = _("children")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.birthdate})"


class Relationship(models.Model):
    PARENT = "parent"  # In Finnish: Vanhempi
    OTHER_GUARDIAN = "other_guardian"  # In Finnish: Muu huoltaja
    OTHER_RELATION = "other_relation"  # In Finnish: Muu läheinen
    ADVOCATE = "advocate"  # In Finnish: Virallinen puolesta-asioija
    TYPE_CHOICES = (
        (PARENT, _("Parent")),
        (OTHER_GUARDIAN, _("Other guardian")),
        (OTHER_RELATION, _("Other relation")),
        (ADVOCATE, _("Advocate")),
    )

    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    child = models.ForeignKey(
        Child,
        verbose_name=_("child"),
        related_name="relationships",
        on_delete=models.CASCADE,
    )
    guardian = models.ForeignKey(
        Guardian,
        verbose_name=_("guardian"),
        on_delete=models.CASCADE,
        related_name="relationships",
    )
    type = models.CharField(
        verbose_name=_("type"),
        choices=TYPE_CHOICES,
        max_length=64,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("relationship")
        verbose_name_plural = _("relationships")
