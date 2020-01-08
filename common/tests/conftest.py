import factory.random
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from freezegun import freeze_time
from graphene.test import Client

from kukkuu.schema import schema
from users.factories import GuardianFactory, UserFactory


@pytest.fixture(autouse=True)
def setup_test_environment(settings):
    factory.random.reseed_random("777")
    with freeze_time("2019-12-12"):
        yield


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


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(schema, context=request)
    client.user = user
    return client
