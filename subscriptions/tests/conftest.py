import pytest
from subscriptions.notifications import NotificationType

from children.factories import ChildWithGuardianFactory
from common.tests.conftest import *  # noqa
from common.tests.utils import create_notification_template_in_language


@pytest.fixture
def child(project):
    return ChildWithGuardianFactory(
        project=project, id="e4ce5bdb-de84-4e7f-a9a4-51cf65cc7d32"
    )


@pytest.fixture
def notification_template_free_spot():
    return create_notification_template_in_language(
        NotificationType.FREE_SPOT,
        "fi",
        subject="Free spot FI",
        body_text="""
        Event FI: {{ event.name }}
        Guardian FI: {{ guardian }}
        Event URL: {{ event_url }}
        Child: {{ child }}
        Occurrence URL: {{ occurrence_url }}
        Subscription created at: {{ subscription.created_at }}
""",
    )
