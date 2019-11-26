import graphene
from django.conf import settings
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Guardian

User = get_user_model()


LanguageEnum = graphene.Enum(
    "Language", [(l[0].upper(), l[0]) for l in settings.LANGUAGES]
)


class GuardianNode(DjangoObjectType):
    language = LanguageEnum()
    email = graphene.String()

    class Meta:
        model = Guardian
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter_for_user(info.context.user).order_by("last_name")

    def resolve_email(self, info, **kwargs):
        return self.user.email


class Query:
    guardians = DjangoConnectionField(GuardianNode)

    @staticmethod
    @login_required
    def resolve_guardians(parent, info, **kwargs):
        return Guardian.objects.filter_for_user(info.context.user)
