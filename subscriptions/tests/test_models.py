from datetime import timedelta

import pytest
from django.utils.timezone import now
from subscriptions.factories import FreeSpotNotificationSubscriptionFactory
from subscriptions.tests.utils import assert_subscriptions

from events.factories import EnrolmentFactory, EventFactory, OccurrenceFactory


@pytest.mark.django_db
def test_enrolling_deletes_same_event_free_spot_subscriptions(
    notification_template_free_spot, child
):
    event = EventFactory(published_at=now())
    occurrence, occurrence_2 = OccurrenceFactory.create_batch(
        2, time=now() + timedelta(days=14), event=event, capacity_override=1,
    )
    EnrolmentFactory(occurrence=occurrence)
    FreeSpotNotificationSubscriptionFactory(
        child=child, occurrence=occurrence
    )  # same event subscription
    other_event_subscription = FreeSpotNotificationSubscriptionFactory(child=child)

    EnrolmentFactory(occurrence=occurrence_2, child=child)

    assert_subscriptions(child, other_event_subscription)
