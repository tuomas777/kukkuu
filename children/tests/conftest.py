import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from graphene.test import Client

from kukkuu.schema import schema
from users.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def api_client():
    return _create_api_client_with_user(AnonymousUser())


@pytest.fixture
def user_api_client(user):
    return _create_api_client_with_user(user)


def _create_api_client_with_user(user):
    request = RequestFactory().post("/graphql")
    request.user = user
    client = Client(schema, context=request)
    client.user = user
    return client
