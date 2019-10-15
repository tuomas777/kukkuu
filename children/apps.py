from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ChildrenConfig(AppConfig):
    name = "children"
    verbose_name = _("children")
