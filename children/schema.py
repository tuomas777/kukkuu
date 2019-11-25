import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from django_ilmoitin.utils import send_notification
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from children.notifications import NotificationType
from users.models import Guardian
from users.schema import GuardianNode, LanguageEnum

from .models import Child, Relationship

User = get_user_model()


class ChildNode(DjangoObjectType):
    class Meta:
        model = Child
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter_for_user(info.context.user).order_by("last_name")


class RelationshipNode(DjangoObjectType):
    class Meta:
        model = Relationship
        interfaces = (relay.Node,)
        fields = ("type", "child", "guardian")


class RelationshipTypeEnum(graphene.Enum):
    PARENT = "parent"
    OTHER_GUARDIAN = "other_guardian"
    OTHER_RELATION = "other_relation"
    ADVOCATE = "advocate"


class RelationshipInput(graphene.InputObjectType):
    type = RelationshipTypeEnum()


class GuardianInput(graphene.InputObjectType):
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    phone_number = graphene.String()
    language = LanguageEnum()


# Unfortunately DjangoObjectTypes do not seem to play well with inheritance,
# so we need duplicate code here.
class ChildMutationOutputNode(ChildNode):
    relationship = graphene.Field(RelationshipNode)

    class Meta:
        model = Child
        interfaces = (relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        return queryset.filter_for_user(info.context.user).order_by("last_name")


class ChildInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birthdate = graphene.Date(required=True)
    postal_code = graphene.String()
    relationship = RelationshipInput()


class SubmitChildrenAndGuardianMutation(graphene.relay.ClientIDMutation):
    class Input:
        children = graphene.List(ChildInput)
        guardian = GuardianInput(required=True)

    children = graphene.List(ChildMutationOutputNode)
    guardian = graphene.Field(GuardianNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        guardian_data = kwargs["guardian"]
        guardian, guardian_created = Guardian.objects.update_or_create(
            user=user,
            defaults=dict(
                first_name=guardian_data["first_name"],
                last_name=guardian_data["last_name"],
                phone_number=guardian_data.get("phone_number", ""),
                language=guardian_data.get("language", ""),
            ),
        )

        # TODO we don't really know the final flow yet, so in the mean time to make
        # development easier we always recreate child here
        Child.objects.filter(relationships__guardian__user=user).delete()

        children = []
        for child in kwargs.get("children", ()):
            relationship_data = child.pop("relationship", {})

            child = Child.objects.create(**child)
            relationship = Relationship.objects.create(
                type=relationship_data.get("type"), child=child, guardian=guardian
            )
            child.relationship = relationship

            children.append(child)

        if guardian_created:
            send_notification(
                guardian.user.email,
                NotificationType.SIGNUP,
                {"children": children, "guardian": guardian},
                guardian.language,
            )

        return SubmitChildrenAndGuardianMutation(children=children, guardian=guardian)


class Query:
    children = DjangoConnectionField(ChildNode)

    @staticmethod
    @login_required
    def resolve_children(parent, info, **kwargs):
        return Child.objects.filter_for_user(info.context.user)
