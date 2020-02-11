from copy import deepcopy

import pytest
from django.core import mail
from graphql_relay import to_global_id

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
def test_event_publish_notification(
    snapshot, staff_api_client, notification_template_event_published_fi, event
):
    guardians = GuardianFactory.create_batch(3, language="fi")
    event_variables = deepcopy(PUBLISH_EVENT_VARIABLES)
    event_variables["input"]["id"] = to_global_id("EventNode", event.id)
    staff_api_client.execute(PUBLISH_EVENT_MUTATION, variables=event_variables)

    assert len(mail.outbox) == len(guardians)
    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_occurrence_enrolment_notifications(
    snapshot,
    user_api_client,
    notification_template_occurrence_unenrolment_fi,
    notification_template_occurrence_enrolment_fi,
    occurrence,
):
    child = ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)
    Enrolment.objects.create(child=child, occurrence=occurrence)
    occurrence.children.remove(child)
    assert len(mail.outbox) == 2
    assert_mails_match_snapshot(snapshot)
