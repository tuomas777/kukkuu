import pytest

from common.tests.conftest import create_api_client_with_user
from common.tests.utils import (
    assert_mails_match_snapshot,
    create_notification_template_in_language,
)
from users.factories import GuardianFactory
from users.notifications import NotificationType


@pytest.fixture
def notification_template_guardian_email_changed_fi():
    return create_notification_template_in_language(
        NotificationType.GUARDIAN_EMAIL_CHANGED,
        "fi",
        subject="Guardian email changed FI",
        body_text="Guardian FI: {{ guardian }}",
    )


@pytest.mark.parametrize(
    "new_email", ("new.email@example.com", "old.email@example.com", None)
)
@pytest.mark.django_db
def test_guardian_changed_email_notification(
    snapshot, new_email, notification_template_guardian_email_changed_fi
):
    guardian = GuardianFactory(
        first_name="Black", last_name="Guardian", email="old.email@example.com"
    )
    api_client = create_api_client_with_user(guardian.user)
    params = {"email": new_email} if new_email else {}

    api_client.execute(
        """
    mutation UpdateMyProfile($input: UpdateMyProfileMutationInput!) {
      updateMyProfile(input: $input) {
        myProfile {
          email
        }
      }
    }
    """,
        variables={"input": {"firstName": "White", **params}},
    )

    assert_mails_match_snapshot(snapshot)
