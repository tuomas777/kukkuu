from copy import deepcopy

import pytest
from django.core import mail
from graphql_relay import to_global_id

from common.tests.utils import (
    assert_mails_match_snapshot,
    create_notification_template_in_language,
)
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
