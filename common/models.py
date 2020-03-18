import uuid

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from parler.managers import TranslatableQuerySet as ParlerTranslatableQuerySet
from parler.models import TranslatableModel as ParlerTranslatableModel
from parler.utils.context import switch_language

from common.utils import update_object
from kukkuu.exceptions import KukkuuGraphQLError


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    id = models.UUIDField(
        verbose_name=_("UUID"), primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True


class TranslatableQuerySet(ParlerTranslatableQuerySet):
    @transaction.atomic
    def create_translatable_object(self, **kwargs):
        translations = kwargs.pop("translations")
        obj = self.create(**kwargs)
        obj.create_or_update_translations(translations)
        return obj


class TranslatableModel(ParlerTranslatableModel):
    objects = TranslatableQuerySet.as_manager()

    class Meta:
        abstract = True

    @transaction.atomic
    def delete_translations(self, language_codes):
        for code in language_codes:
            self.delete_translation(code)

    @transaction.atomic
    def create_or_update_translations(
        self, translations=None, translations_to_delete=None
    ):
        has_default_translation = self.has_translation(settings.LANGUAGE_CODE)
        for translation in translations:
            language_code = translation.pop("language_code")
            if language_code not in settings.PARLER_SUPPORTED_LANGUAGE_CODES:
                continue
            if self.has_translation(language_code):
                with switch_language(self, language_code):
                    update_object(self, translation)
            else:
                self.create_translation(language_code=language_code, **translation)
            if not has_default_translation:
                has_default_translation = language_code == settings.LANGUAGE_CODE
        if not has_default_translation:
            raise KukkuuGraphQLError("Cannot create object without default translation")
        if translations_to_delete:
            if settings.LANGUAGE_CODE in translations_to_delete:
                raise KukkuuGraphQLError("Cannot delete default language code")
            self.delete_translations(translations_to_delete)
