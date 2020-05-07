from copy import deepcopy

import pytest
from django.core import mail
from graphql_relay import to_global_id
from projects.factories import ProjectFactory

from children.factories import ChildWithGuardianFactory
from common.tests.utils import (
    assert_mails_match_snapshot,
    create_notification_template_in_language,
)
from events.models import Enrolment
from events.notifications import NotificationType
from events.tests.test_api import PUBLISH_EVENT_MUTATION, PUBLISH_EVENT_VARIABLES
from users.factories import GuardianFactory


@pytest.fixture
def notification_template_event_published_fi():
    return create_notification_template_in_language(
        NotificationType.EVENT_PUBLISHED,
        "fi",
        subject="Event published FI",
        body_text="""
        Event FI: {{ event }}
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
        Event FI: {{ occurrence.event }}
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
        Event FI: {{ occurrence.event }}
        Guardian FI: {{ guardian }}
        Occurrence: {{ occurrence.time }}
        Child: {{ child }}
""",
    )


@pytest.mark.django_db
def test_event_publish_notification_via_api_call(
    snapshot,
    staff_api_client,
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
    staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=event_variables)

    assert len(mail.outbox) == 5  # 3 children of which one has 3 guardians


@pytest.mark.django_db
def test_occurrence_enrolment_notifications(
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
    occurrence.children.remove(child)
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)
