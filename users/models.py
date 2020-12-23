from typing import List, TYPE_CHECKING

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from guardian.shortcuts import get_objects_for_user
from helusers.models import AbstractUser
from languages.models import Language

from common.models import TimestampedModel, UUIDPrimaryKeyModel

if TYPE_CHECKING:
    from projects.models import Project


class User(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @cached_property
    def administered_projects(self) -> List["Project"]:
        from projects.models import Project  # noqa

        return list(get_objects_for_user(self, "admin", Project))

    def can_administer_project(self, project: "Project") -> bool:
        return project in self.administered_projects


class GuardianQuerySet(models.QuerySet):
    def user_can_view(self, user):
        return self.filter(
            Q(user=user) | Q(children__project__in=user.administered_projects)
        ).distinct()


class Guardian(UUIDPrimaryKeyModel, TimestampedModel):
    user = models.OneToOneField(
        get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE
    )
    first_name = models.CharField(verbose_name=_("first name"), max_length=64)
    last_name = models.CharField(verbose_name=_("last name"), max_length=64)
    phone_number = models.CharField(
        verbose_name=_("phone number"), max_length=64, blank=True
    )
    language = models.CharField(
        verbose_name=_("language"), max_length=10, default=settings.LANGUAGES[0][0]
    )
    email = models.EmailField(
        _("email address"),
        blank=True,
        help_text=_("If left blank, will be populated with the user's email."),
    )
    languages_spoken_at_home = models.ManyToManyField(
        Language,
        verbose_name=_("languages spoken at home"),
        related_name="guardians",
        blank=True,
    )

    objects = GuardianQuerySet.as_manager()

    class Meta:
        verbose_name = _("guardian")
        verbose_name_plural = _("guardians")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = self.user.email
        super().save(*args, **kwargs)
