from copy import deepcopy

import pytest
from graphene.utils.str_converters import to_snake_case
from graphql_relay import to_global_id

from children.factories import ChildWithGuardianFactory
from users.models import Guardian

from ..models import Child, Relationship


def assert_child_matches_data(child_obj, child_data):
    child_data = child_data or {}
    for field_name in ("firstName", "lastName", "birthDate", "postalCode"):
        if field_name in child_data:
            assert (
                str(getattr(child_obj, to_snake_case(field_name)))
                == child_data[field_name]
            )


def assert_relationship_matches_data(relationship_obj, relationship_data):
    relationship_data = relationship_data or {}
    if "type" in relationship_data:
        assert relationship_obj.type == relationship_data.get("type", "").lower()


def assert_guardian_matches_data(guardian_obj, guardian_data):
    guardian_data = guardian_data or {}
    for field_name in ("firstName", "lastName", "phoneNumber"):
        if field_name in guardian_data:
            assert (
                str(getattr(guardian_obj, to_snake_case(field_name)))
                == guardian_data[field_name]
            )
    if "language" in guardian_data:
        assert guardian_obj.language == guardian_data["language"].lower()


SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION = """
mutation submitChildrenAndGuardian($input: SubmitChildrenAndGuardianMutationInput!) {
  submitChildrenAndGuardian(input: $input) {
    children {
      firstName
      lastName
      birthdate
      postalCode
      relationship {
        type
      }
    }
    guardian {
      firstName
      lastName
      phoneNumber
      email
    }
  }
}
"""


CHILDREN_DATA = [
    {
        "firstName": "Matti",
        "lastName": "Mainio",
        "birthdate": "2020-01-01",
        "postalCode": "00840",
        "relationship": {"type": "OTHER_GUARDIAN"},
    },
    {
        "firstName": "Jussi",
        "lastName": "Juonio",
        "birthdate": "2020-02-02",
        "postalCode": "00820",
    },
]


GUARDIAN_DATA = {
    "firstName": "Gulle",
    "lastName": "Guardian",
    "phoneNumber": "777-777777",
    "language": "FI",
}


SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES = {
    "input": {"children": CHILDREN_DATA, "guardian": GUARDIAN_DATA}
}


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
    variables = SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    snapshot.assert_match(executed)

    guardian = Guardian.objects.last()
    assert_guardian_matches_data(guardian, variables["input"]["guardian"])

    for child, child_data in zip(Child.objects.all(), variables["input"]["children"]):
        assert_child_matches_data(child, child_data)
        relationship = Relationship.objects.get(guardian=guardian, child=child)
        assert_relationship_matches_data(relationship, child_data.get("relationship"))


CHILDREN_QUERY = """
query getChildren {
  children {
    edges {
      node {
        firstName
        lastName
        birthdate
        postalCode
        relationships {
          edges {
            node {
              type
              guardian {
                firstName
                lastName
                phoneNumber
                email
              }
            }
          }
        }
      }
    }
  }
}
"""


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


UPDATE_CHILD_MUTATION = """
mutation updateChild($input: UpdateChildMutationInput!) {
  updateChild(input: $input) {
    child {
      firstName
      lastName
      birthdate
      postalCode
    }
  }
}
"""


UPDATE_CHILD_VARIABLES = {
    "input": {
        # "id" needs to be added when actually using these in the mutation
        "firstName": "Matti",
        "lastName": "Mainio",
        "birthdate": "2020-01-01",
        "postalCode": "00840",
        "relationship": {"type": "OTHER_GUARDIAN"},
    }
}


@pytest.mark.django_db
def test_update_child_mutation(snapshot, user_api_client):
    child = ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)

    executed = user_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)

    child.refresh_from_db()
    assert_child_matches_data(child, variables["input"])

    relationship = Relationship.objects.get(
        guardian=user_api_client.user.guardian, child=child
    )
    assert_relationship_matches_data(relationship, variables["input"]["relationship"])


@pytest.mark.django_db
def test_update_child_mutation_wrong_user(snapshot, user_api_client):
    child = ChildWithGuardianFactory()
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)

    executed = user_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "errors" in executed


DELETE_CHILD_MUTATION = """
mutation deleteChild($input: DeleteChildMutationInput!) {
  deleteChild(input: $input) {__typename}
}
"""


@pytest.mark.django_db
def test_delete_child_mutation(snapshot, user_api_client):
    child = ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)
    variables = {"input": {"id": to_global_id("ChildNode", child.id)}}

    executed = user_api_client.execute(DELETE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)
    assert Child.objects.count() == 0


@pytest.mark.django_db
def test_delete_child_mutation_wrong_user(snapshot, user_api_client):
    child = ChildWithGuardianFactory()
    variables = {"input": {"id": to_global_id("ChildNode", child.id)}}

    executed = user_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "errors" in executed
    assert Child.objects.count() == 1
