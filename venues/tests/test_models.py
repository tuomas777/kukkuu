import pytest

from ..factories import VenueFactory
from ..models import Venue


@pytest.mark.django_db
def test_venue_creation():
    VenueFactory()

    assert Venue.objects.count() == 1
