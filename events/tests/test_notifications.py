from copy import deepcopy
from datetime import timedelta

import pytest
from django.core import mail
from django.utils.timezone import now
from graphql_relay import to_global_id
from projects.factories import ProjectFactory

from children.factories import ChildWithGuardianFactory
from common.tests.utils import (
    assert_mails_match_snapshot,
    create_notification_template_in_language,
)
from common.utils import get_global_id
from events.factories import EnrolmentFactory, OccurrenceFactory
from events.models import Enrolment, Occurrence
from events.notifications import NotificationType
from events.tests.test_api import (
    PUBLISH_EVENT_MUTATION,
    PUBLISH_EVENT_VARIABLES,
    UNENROL_OCCURRENCE_MUTATION,
)
from users.factories import GuardianFactory


@pytest.fixture
def notification_template_event_published_fi():
    return create_notification_template_in_language(
        NotificationType.EVENT_PUBLISHED,
        "fi",
        subject="Event published FI",
        body_text="""
        Event FI: {{ event.name }}
        Guardian FI: {{ guardian }}
        Event URL: {{ event_url }}
""",
    )


@pytest.fixture
def notification_template_occurrence_enrolment_fi():
    return create_notification_template_in_language(
        NotificationType.OCCURRENCE_ENROLMENT,
        "fi",
        subject="Occurrence enrolment FI",
        body_text="""
        Event FI: {{ occurrence.event.name }}
        Guardian FI: {{ guardian }}
        Occurrence: {{ occurrence.time }}
        Child: {{ child }}
""",
    )


@pytest.fixture
def notification_template_occurrence_unenrolment_fi():
    return create_notification_template_in_language(
        NotificationType.OCCURRENCE_UNENROLMENT,
        "fi",
        subject="Occurrence unenrolment FI",
        body_text="""
        Event FI: {{ occurrence.event.name }}
        Guardian FI: {{ guardian }}
        Occurrence: {{ occurrence.time }}
        Child: {{ child }}
""",
    )


@pytest.fixture
def notification_template_occurrence_cancelled_fi():
    return create_notification_template_in_language(
        NotificationType.OCCURRENCE_CANCELLED,
        "fi",
        subject="Occurrence cancelled FI",
        body_text="""
        Event FI: {{ occurrence.event.name }}
        Guardian FI: {{ guardian }}
        Occurrence: {{ occurrence.time }}
        Child: {{ child }}
""",
    )


@pytest.mark.django_db
def test_event_publish_notification(
    snapshot,
    project_user_api_client,
    notification_template_event_published_fi,
    unpublished_event,
    project,
):
    GuardianFactory(language="fi")
    children = ChildWithGuardianFactory.create_batch(3, project=project)
    children[1].guardians.set(GuardianFactory.create_batch(3, language="fi"))
    ChildWithGuardianFactory.create_batch(2, project=ProjectFactory(year=2019))

    event_variables = deepcopy(PUBLISH_EVENT_VARIABLES)
    event_variables["input"]["id"] = to_global_id("EventNode", unpublished_event.id)
    project_user_api_client.execute(PUBLISH_EVENT_MUTATION, variables=event_variables)

    assert len(mail.outbox) == 5  # 3 children of which one has 3 guardians


@pytest.mark.django_db
def test_occurrence_enrolment_notifications_on_model_level(
    snapshot,
    user_api_client,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    occurrence,
    project,
):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=user_api_client.user, project=project
    )
    Enrolment.objects.create(child=child, occurrence=occurrence)
    # unenrolling on model level should NOT trigger a notification
    occurrence.children.remove(child)
    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_unenrol_occurrence_notification(
    guardian_api_client,
    snapshot,
    project,
    occurrence,
    notification_template_occurrence_unenrolment_fi,
):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user, project=project,
    )
    EnrolmentFactory(occurrence=occurrence, child=child)
    unenrolment_variables = {
        "input": {
            "occurrenceId": get_global_id(occurrence),
            "childId": get_global_id(child),
        },
    }

    guardian_api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=unenrolment_variables
    )

    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
@pytest.mark.parametrize("is_queryset", (True, False))
def test_occurrence_cancelled_notification(
    snapshot,
    user_api_client,
    notification_template_occurrence_cancelled_fi,
    project,
    is_queryset,
):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=user_api_client.user,
        relationship__guardian__first_name="I Should Receive A Notification",
        project=project,
    )
    other_child = ChildWithGuardianFactory(
        relationship__guardian__first_name="I Should NOT Receive A Notification",
        project=project,
    )

    occurrence = OccurrenceFactory(
        time=now() + timedelta(hours=1), event__project=project
    )
    past_occurrence = OccurrenceFactory(
        time=now() - timedelta(hours=1), event=occurrence.event
    )
    other_event_occurrence = OccurrenceFactory(
        time=now() + timedelta(hours=1), event__project=project
    )

    Enrolment.objects.create(child=child, occurrence=occurrence)
    Enrolment.objects.create(child=child, occurrence=past_occurrence)
    Enrolment.objects.create(child=other_child, occurrence=other_event_occurrence)

    if is_queryset:
        Occurrence.objects.filter(id=occurrence.id).delete()
    else:
        occurrence.delete()

    assert len(mail.outbox) == 1
    assert_mails_match_snapshot(snapshot)
