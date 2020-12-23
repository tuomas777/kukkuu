import graphene
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from projects.schema import ProjectNode

from common.schema import LanguageEnum, set_obj_languages_spoken_at_home
from common.utils import update_object
from kukkuu.exceptions import InvalidEmailFormatError, ObjectDoesNotExistError

from .models import Guardian
from .utils import send_guardian_email_changed_notification

User = get_user_model()


def validate_guardian_data(guardian_data):
    if "email" in guardian_data:
        try:
            validate_email(guardian_data["email"])
        except ValidationError:
            raise InvalidEmailFormatError("Invalid email format")
    return guardian_data


class GuardianNode(DjangoObjectType):
    language = LanguageEnum(required=True)

    class Meta:
        model = Guardian
        fields = (
            "id",
            "created_at",
            "updated_at",
            "user",
            "first_name",
            "last_name",
            "phone_number",
            "language",
            "email",
            "children",
            "relationships",
            "languages_spoken_at_home",
        )
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.user_can_view(info.context.user).order_by("last_name")


class AdminNode(DjangoObjectType):
    projects = DjangoConnectionField(ProjectNode)

    class Meta:
        model = User
        interfaces = (relay.Node,)
        fields = ("projects",)

    @staticmethod
    def resolve_projects(parent, info, **kwargs):
        return parent.administered_projects


class UpdateMyProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        first_name = graphene.String()
        last_name = graphene.String()
        phone_number = graphene.String()
        language = LanguageEnum()
        email = graphene.String()
        languages_spoken_at_home = graphene.List(graphene.NonNull(graphene.ID))

    my_profile = graphene.Field(GuardianNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        try:
            guardian = user.guardian
        except Guardian.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)

        languages_spoken_at_home = kwargs.pop("languages_spoken_at_home", [])
        validate_guardian_data(kwargs)

        old_email = guardian.email
        update_object(guardian, kwargs)
        set_obj_languages_spoken_at_home(info, guardian, languages_spoken_at_home)

        if guardian.email != old_email:
            send_guardian_email_changed_notification(guardian)

        return UpdateMyProfileMutation(my_profile=guardian)


class Query:
    guardians = DjangoConnectionField(GuardianNode)
    my_profile = graphene.Field(GuardianNode)
    my_admin_profile = graphene.Field(AdminNode)

    @staticmethod
    @login_required
    def resolve_guardians(parent, info, **kwargs):
        return Guardian.objects.user_can_view(info.context.user)

    @staticmethod
    @login_required
    def resolve_my_profile(parent, info, **kwargs):
        return Guardian.objects.filter(user=info.context.user).first()

    @staticmethod
    @login_required
    def resolve_my_admin_profile(parent, info, **kwargs):
        return info.context.user


class Mutation:
    update_my_profile = UpdateMyProfileMutation.Field()
