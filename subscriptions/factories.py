import factory
from subscriptions.models import FreeSpotNotificationSubscription

from children.factories import ChildFactory
from events.factories import OccurrenceFactory


class FreeSpotNotificationSubscriptionFactory(factory.django.DjangoModelFactory):
    occurrence = factory.SubFactory(OccurrenceFactory)
    child = factory.SubFactory(ChildFactory)

    class Meta:
        model = FreeSpotNotificationSubscription
