import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from graphene import relay
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

from users.models import Guardian
from users.schema import GuardianNode

from .models import Child, Relationship

User = get_user_model()


class ChildNode(DjangoObjectType):
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
    email = graphene.String(required=True)
    phone_number = graphene.String()


class SubmitChildMutation(graphene.relay.ClientIDMutation):
    class Input:
        child = ChildInput(required=True)
        relationship = RelationshipInput()
        guardian = GuardianInput(required=True)

    child = graphene.Field(ChildNode)
    relationship = graphene.Field(RelationshipNode)
    guardian = graphene.Field(GuardianNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        user = info.context.user

        # TODO we don't really know the final flow yet, so in the mean time to make
        # development easier we always recreate child here
        Child.objects.filter(relationships__guardian__user=user).delete()
        child = Child.objects.create(**kwargs["child"])

        guardian_data = kwargs["guardian"]
        guardian, _ = Guardian.objects.update_or_create(
            user=user,
            defaults=dict(
                first_name=guardian_data["first_name"],
                last_name=guardian_data["last_name"],
                email=guardian_data["email"],
                phone_number=guardian_data.get("phone_number", ""),
            ),
        )

        if "relationship" in kwargs:
            relationship_type = kwargs["relationship"].get("type")
        else:
            relationship_type = None
        relationship = Relationship.objects.create(
            type=relationship_type, child=child, guardian=guardian
        )

        return SubmitChildMutation(
            child=child, relationship=relationship, guardian=guardian
        )


class Query:
    children = DjangoConnectionField(ChildNode)

    @staticmethod
    @login_required
    def resolve_children(parent, info, **kwargs):
        return Child.objects.filter_for_user(info.context.user)
