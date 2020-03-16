from django.db import transaction

from kukkuu import __version__
from kukkuu.settings import REVISION


def update_object(obj, data):
    if not data:
        return
    for k, v in data.items():
        setattr(obj, k, v)
    obj.save()


@transaction.atomic
def update_object_with_translations(model, model_data):
    translations_input = model_data.pop("translations", None)
    delete_translations_input = model_data.pop("delete_translations", None)

    if translations_input or delete_translations_input:
        model.create_or_update_translations(
            translations_input, delete_translations_input
        )
    update_object(model, model_data)


def get_api_version():
    return " | ".join((__version__, REVISION.decode("utf-8")))
