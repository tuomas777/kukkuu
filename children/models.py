import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Child(models.Model):
    uuid = models.UUIDField(
        verbose_name=_("UUID"), primary_key=True, default=uuid.uuid4
    )
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=64)
    last_name = models.CharField(verbose_name=_("last name"), max_length=64)
    birthdate = models.DateField(verbose_name=_("birthdate"))
    social_security_number_hash = models.CharField(
        verbose_name=_("social security number hash"), max_length=255, editable=False
    )
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

    def _set_social_security_number_hash(self, social_security_number):
        self.social_security_number_hash = make_password(social_security_number)

    social_security_number = property(None, _set_social_security_number_hash)


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
