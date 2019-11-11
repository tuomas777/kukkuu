import pytest
from graphene.utils.str_converters import to_snake_case

from children.factories import ChildWithGuardianFactory
from users.models import Guardian

from ..models import Child, Relationship

CHILDREN_QUERY = """
query getChildren {
  children {
    edges {
      node {
        firstName
        lastName
        birthdate
        relationships {
          edges {
            node {
              type
              guardian {
                firstName
                lastName
                email
                phoneNumber
              }
            }
          }
        }
      }
    }
  }
}
"""


SUBMIT_CHILD_MUTATION = """
mutation submitChild($input: SubmitChildMutationInput!) {
  submitChild(input: $input) {
    child {
      firstName
      lastName
      birthdate
    }
    relationship {
      type
    }
    guardian {
      firstName
      lastName
      email
      phoneNumber
    }
  }
}
"""


CHILD_DATA = {"firstName": "Matti", "lastName": "Mainio", "birthdate": "2020-05-05"}


GUARDIAN_DATA = {
    "firstName": "Jussi",
    "lastName": "Juonio",
    "email": "jussi@example.com",
    "phoneNumber": "777-777777",
}


SUBMIT_CHILD_VARIABLES = {
    "input": {
        "child": CHILD_DATA,
        "guardian": GUARDIAN_DATA,
        "relationship": {"type": "PARENT"},
    }
}


def to_snake_dict(d):
    return {to_snake_case(k): v for k, v in d.items()}


@pytest.mark.django_db
def test_submit_child_unauthenticated(api_client):
    executed = api_client.execute(
        SUBMIT_CHILD_MUTATION, variables=SUBMIT_CHILD_VARIABLES
    )

    # TODO add better check when we have error codes
    assert "errors" in executed


@pytest.mark.django_db
def test_submit_child_authenticated(snapshot, user_api_client):
    executed = user_api_client.execute(
        SUBMIT_CHILD_MUTATION, variables=SUBMIT_CHILD_VARIABLES
    )

    snapshot.assert_match(executed)

    # check that everything is created properly to the db
    child = Child.objects.get(**to_snake_dict(CHILD_DATA))
    guardian = Guardian.objects.get(**to_snake_dict(GUARDIAN_DATA))
    Relationship.objects.get(type=Relationship.PARENT, child=child, guardian=guardian)


@pytest.mark.django_db
def test_children_query_unauthenticated(api_client):
    executed = api_client.execute(CHILDREN_QUERY)

    # TODO add better check when we have error codes
    assert "errors" in executed


@pytest.mark.django_db
def test_children_query_normal_user(snapshot, user_api_client):
    ChildWithGuardianFactory()
    ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)

    executed = user_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_children_query_staff_user(snapshot, staff_api_client):
    ChildWithGuardianFactory()
    ChildWithGuardianFactory(relationship__guardian__user=staff_api_client.user)

    executed = staff_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)
