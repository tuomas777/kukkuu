import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Child(models.Model):
    id = models.UUIDField(
        verbose_name=_("UUID"), primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=64)
    last_name = models.CharField(verbose_name=_("last name"), max_length=64)
    birthdate = models.DateField(verbose_name=_("birthdate"))
    users = models.ManyToManyField(
        get_user_model(),
        verbose_name=_("users"),
        related_name="children",
        through="children.Relationship",
        blank=True,
    )

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
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_("user"),
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
