import shutil

import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client

from events.factories import EventFactory, OccurrenceFactory
from kukkuu.schema import schema
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
def event():
    return EventFactory()


@pytest.fixture
def venue():
    return VenueFactory()


@pytest.fixture
def occurrence():
    return OccurrenceFactory()


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(schema, context=request)
    client.user = user
    return client
