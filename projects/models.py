from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Project(TranslatableModel):
    year = models.PositiveSmallIntegerField(verbose_name=_("year"), unique=True)
    users = models.ManyToManyField(
        get_user_model(), verbose_name=_("users"), related_name="projects", blank=True
    )
    translations = TranslatedFields(
        name=models.CharField(verbose_name=_("name"), max_length=255)
    )

    class Meta:
        verbose_name = _("project")
        verbose_name_plural = _("projects")
        ordering = ["year"]

    def __str__(self):
        return f"#{self.pk} {self.year}"

    def can_user_administer(self, user):
        return user.projects.filter(pk=self.pk).exists()
