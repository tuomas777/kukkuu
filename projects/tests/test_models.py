import pytest
from django.contrib.auth import get_user_model

from children.factories import ChildFactory
from events.factories import EventFactory
from users.factories import UserFactory
from venues.factories import VenueFactory

User = get_user_model()


@pytest.mark.django_db
def test_project_creation(project):
    ChildFactory(project=project)
    EventFactory(project=project)
    VenueFactory(project=project)
    user = UserFactory()
    user.projects.add(project)
    assert project.events.count() == 1
    assert project.venues.count() == 1
    assert project.users.count() == 1
