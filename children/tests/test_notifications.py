import pytest
from django.core import mail
from django_ilmoitin.models import NotificationTemplate

from children.tests.test_api import (
    SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
    SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
)
from users.factories import GuardianFactory

from ..notifications import NotificationType


def assert_mails_match_snapshot(snapshot):
    snapshot.assert_match(
        [f"{m.from_email}|{m.to}|{m.subject}|{m.body}" for m in mail.outbox]
    )


@pytest.fixture
def notification_template_signup_fi():
    return NotificationTemplate.objects.language("fi").create(
        type=NotificationType.SIGNUP,
        subject="SIGNUP-notifikaation aihe",
        body_text="""
SIGNUP-notifikaation sisältö tekstimuodossa.
Lapset: {{ children }}
Huoltajat: {{ guardian }}
""",
    )


@pytest.mark.django_db
def test_signup_notification(
    snapshot, user_api_client, notification_template_signup_fi
):
    user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    assert_mails_match_snapshot(snapshot)


@pytest.mark.django_db
def test_signup_notification_guardian_exists(
    snapshot, user_api_client, notification_template_signup_fi
):
    GuardianFactory(user=user_api_client.user)

    user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    assert len(mail.outbox) == 0
