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


SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION = """
mutation submitChildrenAndGuardian($input: SubmitChildrenAndGuardianMutationInput!) {
  submitChildrenAndGuardian(input: $input) {
    children {
      firstName
      lastName
      birthdate
      relationship {
        type
      }
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


CHILDREN_DATA = [
    {
        "firstName": "Matti",
        "lastName": "Mainio",
        "birthdate": "2020-01-01",
        "relationship": {"type": "OTHER_GUARDIAN"},
    },
    {"firstName": "Jussi", "lastName": "Juonio", "birthdate": "2020-02-02"},
]


GUARDIAN_DATA = {
    "firstName": "Gulle",
    "lastName": "Guardian",
    "email": "gulle@example.com",
    "phoneNumber": "777-777777",
}


SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES = {
    "input": {"children": CHILDREN_DATA, "guardian": GUARDIAN_DATA}
}


def to_snake_dict(d):
    return {to_snake_case(k): v for k, v in d.items()}


@pytest.mark.django_db
def test_submit_child_unauthenticated(api_client):
    executed = api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    # TODO add better check when we have error codes
    assert "errors" in executed


@pytest.mark.django_db
def test_submit_child_authenticated(snapshot, user_api_client):
    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    snapshot.assert_match(executed)

    # check that everything is created properly to the db
    guardian = Guardian.objects.get(**to_snake_dict(GUARDIAN_DATA))
    for child_data in CHILDREN_DATA:
        relationship_type_name = child_data.pop("relationship", {}).get("type", "")
        relationship_type = getattr(Relationship, relationship_type_name, None)
        child = Child.objects.get(**to_snake_dict(child_data))
        Relationship.objects.get(type=relationship_type, child=child, guardian=guardian)


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
