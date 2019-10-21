import graphene
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.crypto import get_random_string
from graphene_django.types import DjangoObjectType

from users.models import Guardian

from .models import Child, Relationship

User = get_user_model()


class ChildType(DjangoObjectType):
    class Meta:
        model = Child


class ChildInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    birthdate = graphene.Date(required=True)


# this class cannot be named just RelationshipType because of graphene-django
# https://github.com/graphql-python/graphene-django/issues/185
class RelationshipObjectType(DjangoObjectType):
    class Meta:
        model = Relationship
        fields = ("type", "child", "guardian")


class RelationshipTypeEnum(graphene.Enum):
    PARENT = "parent"
    OTHER_GUARDIAN = "other_guardian"
    OTHER_RELATION = "other_relation"
    ADVOCATE = "advocate"


class RelationshipInput(graphene.InputObjectType):
    type = RelationshipTypeEnum()


class GuardianType(DjangoObjectType):
    class Meta:
        model = Guardian


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

    child = graphene.Field(ChildType)
    relationship = graphene.Field(RelationshipObjectType)
    guardian = graphene.Field(GuardianType)

    @classmethod
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # TODO we'll probably need to check somehow if the child already exists
        child = Child.objects.create(**kwargs["child"])

        # TODO change this to logged in user once we have authentication in place
        user = User.objects.create(
            first_name=get_random_string(),
            last_name=get_random_string(),
            username=get_random_string(),
        )

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
