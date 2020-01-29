import graphene
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from common.utils import update_object
from kukkuu.exceptions import KukkuuGraphQLError

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
        return queryset.user_can_view(info.context.user).order_by("last_name")

    def resolve_email(self, info, **kwargs):
        return self.user.email


class UpdateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        language = LanguageEnum()

    my_profile = graphene.Field(GuardianNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        try:
            guardian = user.guardian
        except Guardian.DoesNotExist as e:
            raise KukkuuGraphQLError(e)

        update_object(guardian, kwargs)

        return UpdateMyProfileMutation(my_profile=guardian)


class Query:
    guardians = DjangoConnectionField(GuardianNode)
    my_profile = graphene.Field(GuardianNode)

    @staticmethod
    @login_required
    def resolve_guardians(parent, info, **kwargs):
        return Guardian.objects.user_can_view(info.context.user)

    @staticmethod
    @login_required
    def resolve_my_profile(parent, info, **kwargs):
        return Guardian.objects.filter(user=info.context.user).first()


class Mutation:
    update_my_profile = UpdateMyProfileMutation.Field()
