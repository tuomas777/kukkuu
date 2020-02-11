import pytest
from django.contrib.auth import get_user_model

from children.factories import ChildFactory
from venues.models import Venue

from ..factories import EventFactory, OccurrenceFactory
from ..models import Enrolment, Event, Occurrence

User = get_user_model()


@pytest.mark.django_db
def test_event_creation():
    EventFactory()

    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_occurrence_creation():
    OccurrenceFactory()

    assert Occurrence.objects.count() == 1
    assert Event.objects.count() == 1
    assert Venue.objects.count() == 1


@pytest.mark.django_db
def test_enrolment_creation(occurrence):
    child = ChildFactory()
    occurrence.children.add(child)
    assert occurrence.children.count() == 1
    assert child.occurrences.count() == 1
    assert Enrolment.objects.count() == 1
