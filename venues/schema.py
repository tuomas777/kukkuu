import graphene
from django.apps import apps
from django.db import transaction
from django.db.models import Count
from django.utils.translation import get_language
from graphene import relay
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphql_jwt.decorators import login_required
from projects.models import Project

from common.utils import (
    get_obj_if_user_can_administer,
    project_user_required,
    update_object_with_translations,
)
from users.schema import LanguageEnum
from venues.models import Venue

VenueTranslation = apps.get_model("venues", "VenueTranslation")


class VenueTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)

    class Meta:
        model = VenueTranslation
        exclude = ("id", "master")


class VenueNode(DjangoObjectType):
    name = graphene.String()
    description = graphene.String()
    address = graphene.String()
    accessibility_info = graphene.String()
    arrival_instructions = graphene.String()
    additional_info = graphene.String()
    wc_and_facilities = graphene.String()
    www_url = graphene.String()

    class Meta:
        model = Venue
        interfaces = (relay.Node,)

    @classmethod
    @login_required
    # TODO: For now only logged in users can see venues
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return queryset.order_by("-created_at").language(lang)

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return super().get_node(info, id)

    def resolve_occurrences(self, info, **kwargs):
        return (
            self.occurrences.annotate(
                enrolment_count=Count("enrolments", distinct=True)
            )
            .select_related("event")
            .order_by("time")
        )


class VenueTranslationsInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    language_code = LanguageEnum(required=True)
    address = graphene.String()
    accessibility_info = graphene.String()
    arrival_instructions = graphene.String()
    additional_info = graphene.String()
    www_url = graphene.String()
    wc_and_facilities = graphene.String()


class AddVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        translations = graphene.List(VenueTranslationsInput)
        project_id = graphene.GlobalID()

    venue = graphene.Field(VenueNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        kwargs["project_id"] = get_obj_if_user_can_administer(
            info, kwargs["project_id"], Project
        ).pk
        venue = Venue.objects.create_translatable_object(**kwargs)
        return AddVenueMutation(venue=venue)


class UpdateVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        translations = graphene.List(VenueTranslationsInput)
        project_id = graphene.GlobalID(required=False)

    venue = graphene.Field(VenueNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        project_global_id = kwargs.pop("project_id", None)
        if project_global_id:
            kwargs["project_id"] = get_obj_if_user_can_administer(
                info, project_global_id, Project
            )
        venue = get_obj_if_user_can_administer(info, kwargs.pop("id"), Venue)
        update_object_with_translations(venue, kwargs)

        return UpdateVenueMutation(venue=venue)


class DeleteVenueMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        venue = get_obj_if_user_can_administer(info, kwargs["id"], Venue)
        venue.delete()
        return DeleteVenueMutation()


class Query:
    venue = relay.Node.Field(VenueNode)
    venues = DjangoConnectionField(VenueNode)


class Mutation:
    add_venue = AddVenueMutation.Field()
    update_venue = UpdateVenueMutation.Field()
    delete_venue = DeleteVenueMutation.Field()
