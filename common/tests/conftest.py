import shutil

import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.utils import timezone
from freezegun import freeze_time
from graphene.test import Client
from projects.models import Project

from children.factories import ChildWithGuardianFactory
from events.factories import EventFactory, OccurrenceFactory
from kukkuu.schema import schema
from kukkuu.views import SentryGraphQLView
from users.factories import GuardianFactory, UserFactory
from venues.factories import VenueFactory


@pytest.fixture(autouse=True)
def setup_test_environment(settings):
    factory.random.reseed_random("777")
    settings.DEFAULT_FROM_EMAIL = "kukkuu@example.com"
    settings.ILMOITIN_TRANSLATED_FROM_EMAIL = {}
    settings.MEDIA_ROOT = "test_media"
    with freeze_time("2020-12-12"):
        yield
    shutil.rmtree("test_media", ignore_errors=True)


@pytest.fixture
def project():
    return Project.objects.get_or_create(year=2020)[0]


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def api_client():
    return _create_api_client_with_user(AnonymousUser())


@pytest.fixture
def user_api_client():
    return _create_api_client_with_user(UserFactory())


@pytest.fixture
def staff_api_client():
    return _create_api_client_with_user(UserFactory(is_staff=True))


@pytest.fixture
def guardian_api_client():
    return _create_api_client_with_user(UserFactory(guardian=GuardianFactory()))


@pytest.fixture
def child_with_random_guardian(project):
    return ChildWithGuardianFactory(project=project)


@pytest.fixture
def child_with_user_guardian(guardian_api_client, project):
    return ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user, project=project
    )


@pytest.fixture
def event(project):
    return EventFactory(published_at=timezone.now(), project=project)


@pytest.fixture
def unpublished_event(project):
    return EventFactory(project=project)


@pytest.fixture
def venue(project):
    return VenueFactory(project=project)


@pytest.fixture
def occurrence(venue, event):
    return OccurrenceFactory(time=timezone.now(), venue=venue, event=event)


@pytest.fixture
def unpublished_occurrence(venue, unpublished_event):
    return OccurrenceFactory(time=timezone.now(), venue=venue, event=unpublished_event)


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(
        schema, context=request, format_error=SentryGraphQLView.format_error
    )
    client.user = user
    return client
