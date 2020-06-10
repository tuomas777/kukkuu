import graphene
from django.apps import apps
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.translation import get_language
from graphene import Connection, relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_file_upload.scalars import Upload
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id
from projects.models import Project

from children.models import Child
from children.schema import ChildNode
from common.schema import LanguageEnum
from common.utils import (
    get_obj_if_user_can_administer,
    project_user_required,
    update_object,
    update_object_with_translations,
)
from events.filters import OccurrenceFilter
from events.models import Enrolment, Event, Occurrence
from kukkuu.exceptions import (
    ChildAlreadyJoinedEventError,
    EventAlreadyPublishedError,
    IneligibleOccurrenceEnrolment,
    ObjectDoesNotExistError,
    OccurrenceIsFullError,
    PastOccurrenceError,
)
from venues.models import Venue

EventTranslation = apps.get_model("events", "EventTranslation")


def validate_enrolment(child, occurrence):
    if child.project != occurrence.event.project:
        raise IneligibleOccurrenceEnrolment(
            "Child does not belong to the project event"
        )
    if child.occurrences.filter(event=occurrence.event).exists():
        raise ChildAlreadyJoinedEventError("Child already joined this event")
    if occurrence.enrolments.count() >= occurrence.event.capacity_per_occurrence:
        raise OccurrenceIsFullError("Maximum enrolments created")
    if occurrence.time < timezone.now():
        raise PastOccurrenceError("Cannot join occurrence in the past")


class EventParticipantsPerInvite(graphene.Enum):
    CHILD_AND_GUARDIAN = "child_and_guardian"
    FAMILY = "family"


class EventTranslationType(DjangoObjectType):
    language_code = LanguageEnum(required=True)

    class Meta:
        model = EventTranslation
        exclude = ("id", "master")


class EventNode(DjangoObjectType):
    name = graphene.String()
    description = graphene.String()
    short_description = graphene.String()
    image_alt_text = graphene.String()
    participants_per_invite = EventParticipantsPerInvite(required=True)

    class Meta:
        model = Event
        interfaces = (relay.Node,)
        filter_fields = ("project_id",)

    @classmethod
    @login_required
    # TODO: For now only logged in users can see events
    def get_queryset(cls, queryset, info):
        lang = get_language()
        return (
            queryset.user_can_view(info.context.user)
            .order_by("-created_at")
            .language(lang)
        )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return super().get_node(info, id)

    def resolve_image(self, info, **kwargs):
        if self.image:
            return info.context.build_absolute_uri(self.image.url)
        return ""

    def resolve_occurrences(self, info, **kwargs):
        return self.occurrences.annotate(
            enrolment_count=Count("enrolments", distinct=True)
        ).order_by("time")


class EventConnection(Connection):
    class Meta:
        node = EventNode


class OccurrenceNode(DjangoObjectType):
    remaining_capacity = graphene.Int()
    occurrence_language = LanguageEnum(required=True)
    enrolment_count = graphene.Int(required=True)

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        return (
            queryset.user_can_view(info.context.user)
            .annotate(enrolment_count=Count("enrolments", distinct=True))
            .order_by("time")
        )

    @classmethod
    @login_required
    def get_node(cls, info, id):
        return super().get_node(info, id)

    def resolve_remaining_capacity(self, info, **kwargs):
        return self.event.capacity_per_occurrence - self.get_enrolment_count()

    def resolve_enrolment_count(self, info, **kwargs):
        return self.get_enrolment_count()

    class Meta:
        model = Occurrence
        interfaces = (relay.Node,)
        filterset_class = OccurrenceFilter


class EnrolmentNode(DjangoObjectType):
    class Meta:
        model = Enrolment
        interfaces = (relay.Node,)
        fields = ("occurrence", "child", "created_at")

    @classmethod
    @login_required
    def get_queryset(cls, queryset, info):
        user = info.context.user
        return queryset.filter(
            Q(child__guardians__user=info.context.user) | Q(child__project__users=user)
        ).distinct()


class EventTranslationsInput(graphene.InputObjectType):
    name = graphene.String()
    short_description = graphene.String()
    description = graphene.String()
    image_alt_text = graphene.String()
    language_code = LanguageEnum(required=True)


class AddEventMutation(graphene.relay.ClientIDMutation):
    class Input:
        translations = graphene.List(EventTranslationsInput)
        duration = graphene.Int()
        participants_per_invite = EventParticipantsPerInvite(required=True)
        capacity_per_occurrence = graphene.Int(required=True)
        image = Upload()
        project_id = graphene.GlobalID()

    event = graphene.Field(EventNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        kwargs["project_id"] = get_obj_if_user_can_administer(
            info, kwargs.pop("project_id"), Project
        ).pk
        event = Event.objects.create_translatable_object(**kwargs)
        return AddEventMutation(event=event)


class UpdateEventMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        duration = graphene.Int()
        participants_per_invite = EventParticipantsPerInvite()
        capacity_per_occurrence = graphene.Int()
        image = Upload()
        translations = graphene.List(EventTranslationsInput)
        project_id = graphene.GlobalID(required=False)

    event = graphene.Field(EventNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        project_global_id = kwargs.pop("project_id", None)
        if project_global_id:
            kwargs["project_id"] = get_obj_if_user_can_administer(
                info, project_global_id, Project
            ).pk

        event = get_obj_if_user_can_administer(info, kwargs.pop("id"), Event)
        update_object_with_translations(event, kwargs)
        return UpdateEventMutation(event=event)


class DeleteEventMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        event = get_obj_if_user_can_administer(info, kwargs["id"], Event)
        event.delete()
        return DeleteEventMutation()


class EnrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_id = graphene.GlobalID(description="Occurrence id of event")
        child_id = graphene.GlobalID(description="Guardian's child id")

    enrolment = graphene.Field(EnrolmentNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence_id = from_global_id(kwargs["occurrence_id"])[1]
        child_id = from_global_id(kwargs["child_id"])[1]
        user = info.context.user
        try:
            occurrence = Occurrence.objects.get(pk=occurrence_id)
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        try:
            child = Child.objects.user_can_update(user).get(pk=child_id)
        except Child.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        validate_enrolment(child, occurrence)
        enrolment = Enrolment.objects.create(child=child, occurrence=occurrence)

        return EnrolOccurrenceMutation(enrolment=enrolment)


class UnenrolOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        occurrence_id = graphene.GlobalID(description="Occurrence id of event")
        child_id = graphene.GlobalID(description="Guardian's child id")

    occurrence = graphene.Field(OccurrenceNode)
    child = graphene.Field(ChildNode)

    @classmethod
    @login_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence_id = from_global_id(kwargs["occurrence_id"])[1]
        child_id = from_global_id(kwargs["child_id"])[1]
        user = info.context.user
        try:
            child = Child.objects.user_can_update(user).get(pk=child_id)
        except Child.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        try:
            occurrence = child.occurrences.get(pk=occurrence_id)
            occurrence.children.remove(child)
        except Occurrence.DoesNotExist as e:
            raise ObjectDoesNotExistError(e)
        return UnenrolOccurrenceMutation(child=child, occurrence=occurrence)


class AddOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        time = graphene.DateTime(required=True)
        event_id = graphene.GlobalID()
        venue_id = graphene.GlobalID()
        occurrence_language = LanguageEnum()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        kwargs["event_id"] = get_obj_if_user_can_administer(
            info, kwargs["event_id"], Event
        ).pk
        kwargs["venue_id"] = get_obj_if_user_can_administer(
            info, kwargs["venue_id"], Venue
        ).pk

        occurrence = Occurrence.objects.create(**kwargs)

        # needed because enrolment_count is an annotated field
        occurrence.enrolment_count = 0

        return AddOccurrenceMutation(occurrence=occurrence)


class UpdateOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()
        time = graphene.DateTime()
        event_id = graphene.GlobalID(required=False)
        venue_id = graphene.GlobalID(required=False)
        occurrence_language = LanguageEnum()

    occurrence = graphene.Field(OccurrenceNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_obj_if_user_can_administer(info, kwargs.pop("id"), Occurrence)

        if kwargs.get("event_id"):
            kwargs["event_id"] = get_obj_if_user_can_administer(
                info, kwargs["event_id"], Event
            ).pk

        if kwargs.get("venue_id"):
            kwargs["venue_id"] = get_obj_if_user_can_administer(
                info, kwargs["venue_id"], Venue
            ).pk

        update_object(occurrence, kwargs)
        return UpdateOccurrenceMutation(occurrence=occurrence)


class DeleteOccurrenceMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        occurrence = get_obj_if_user_can_administer(info, kwargs["id"], Occurrence)
        occurrence.delete()
        return DeleteOccurrenceMutation()


class PublishEventMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.GlobalID()

    event = graphene.Field(EventNode)

    @classmethod
    @project_user_required
    @transaction.atomic
    def mutate_and_get_payload(cls, root, info, **kwargs):
        event = get_obj_if_user_can_administer(info, kwargs["id"], Event)

        if event.is_published():
            raise EventAlreadyPublishedError("Event is already published")

        event.publish()
        return PublishEventMutation(event=event)


class Query:
    events = DjangoFilterConnectionField(EventNode)
    occurrences = DjangoFilterConnectionField(OccurrenceNode)

    event = relay.Node.Field(EventNode)
    occurrence = relay.Node.Field(OccurrenceNode)


class Mutation:
    add_event = AddEventMutation.Field()
    update_event = UpdateEventMutation.Field()
    delete_event = DeleteEventMutation.Field()
    publish_event = PublishEventMutation.Field()

    add_occurrence = AddOccurrenceMutation.Field()
    update_occurrence = UpdateOccurrenceMutation.Field()
    delete_occurrence = DeleteOccurrenceMutation.Field()
    enrol_occurrence = EnrolOccurrenceMutation.Field()
    unenrol_occurrence = UnenrolOccurrenceMutation.Field()
