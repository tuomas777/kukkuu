from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from helusers.models import AbstractUser

from common.models import TimestampedModel, UUIDPrimaryKeyModel


class User(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class GuardianQuerySet(models.QuerySet):
    def user_can_view(self, user):
        # TODO we'll probably need more fine-grained control than this
        if user.is_staff:
            return self
        else:
            return self.filter(user=user)


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
    email = models.EmailField(_("email address"), blank=True)

    objects = GuardianQuerySet.as_manager()

    class Meta:
        verbose_name = _("guardian")
        verbose_name_plural = _("guardians")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_email_in_use(self):
        return self.email or self.user.email
