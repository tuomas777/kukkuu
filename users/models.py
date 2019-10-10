from django.db import models
from django.utils.translation import ugettext_lazy as _
from helusers.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(
        verbose_name=_("phone number"), max_length=64, blank=True
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
