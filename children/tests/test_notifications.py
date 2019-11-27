from copy import deepcopy

import pytest
from django.core import mail
from django_ilmoitin.models import NotificationTemplate
from parler.utils.context import switch_language

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


def create_notification_template_in_language(
    notification_type, language, **translations
):
    try:
        template = NotificationTemplate.objects.get(type=notification_type)
    except NotificationTemplate.DoesNotExist:
        template = NotificationTemplate(type=notification_type)
    with switch_language(template, language):
        for field, value in translations.items():
            setattr(template, field, value)
            template.save()

    return template


@pytest.fixture
def notification_template_signup_fi():
    return create_notification_template_in_language(
        NotificationType.SIGNUP,
        "fi",
        subject="SIGNUP-notifikaation aihe",
        body_text="""
SIGNUP-notifikaation sisältö tekstimuodossa.
Lapset: {{ children }}
Huoltaja: {{ guardian }}
""",
    )


@pytest.fixture
def notification_template_signup_en():
    return create_notification_template_in_language(
        NotificationType.SIGNUP,
        "en",
        subject="SIGNUP notification subject",
        body_text="""
SIGNUP notification body text.
Children: {{ children }}
Guardian: {{ guardian }}
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


@pytest.mark.parametrize("language", ["FI", "EN", "SV"])
@pytest.mark.django_db
def test_signup_notification_language(
    snapshot,
    user_api_client,
    language,
    notification_template_signup_fi,
    notification_template_signup_en,
):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["guardian"]["language"] = language

    user_api_client.execute(SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables)

    # SV should be the same as FI as there are no SV translation
    assert_mails_match_snapshot(snapshot)
