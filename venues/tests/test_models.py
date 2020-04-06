import pytest

from ..factories import VenueFactory
from ..models import Venue


@pytest.mark.django_db
def test_venue_creation(project):
    VenueFactory(project=project)

    assert Venue.objects.count() == 1
