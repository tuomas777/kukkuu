import pytest
from django.contrib.auth import get_user_model

from ..factories import EventFactory, OccurrenceFactory
from ..models import Event, Occurrence

User = get_user_model()


@pytest.mark.django_db
def test_event_creation():
    EventFactory()

    assert Event.objects.count() == 1


@pytest.mark.django_db
def test_occurrence_creation():
    OccurrenceFactory()

    assert Occurrence.objects.count() == 1
