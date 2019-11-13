from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from .models import Guardian

User = get_user_model()


class GuardianNode(DjangoObjectType):
    class Meta:
        model = Guardian
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter_for_user(info.context.user).order_by("last_name")


class Query:
    guardians = DjangoConnectionField(GuardianNode)

    @staticmethod
    @login_required
    def resolve_guardians(parent, info, **kwargs):
        return Guardian.objects.filter_for_user(info.context.user)
