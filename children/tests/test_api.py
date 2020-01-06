from copy import deepcopy

import pytest
from graphene.utils.str_converters import to_snake_case
from graphql_relay import to_global_id

from children.factories import ChildWithGuardianFactory
from common.tests.utils import assert_permission_denied
from users.models import Guardian

from ..models import Child, Relationship


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


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
mutation SubmitChildrenAndGuardian($input: SubmitChildrenAndGuardianMutationInput!) {
  submitChildrenAndGuardian(input: $input) {
    children {
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


def test_submit_children_and_guardian_unauthenticated(api_client):
    executed = api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    assert_permission_denied(executed)


def test_submit_children_and_guardian(snapshot, user_api_client):
    variables = SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    snapshot.assert_match(executed)

    guardian = Guardian.objects.last()
    assert_guardian_matches_data(guardian, variables["input"]["guardian"])

    for child, child_data in zip(
        Child.objects.order_by("birthdate"), variables["input"]["children"]
    ):
        assert_child_matches_data(child, child_data)
        relationship = Relationship.objects.get(guardian=guardian, child=child)
        assert_relationship_matches_data(relationship, child_data.get("relationship"))


def test_submit_children_and_guardian_one_child_required(snapshot, user_api_client):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"] = []

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert "At least one child is required." in str(executed["errors"])


def test_submit_children_and_guardian_postal_code_validation(user_api_client):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"][0]["postalCode"] = "1234x"

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert "Postal code must be 5 digits" in str(executed["errors"])


def test_submit_children_and_guardian_postal_code_can_be_empty(user_api_client):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"][0]["postalCode"] = ""

    user_api_client.execute(SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables)

    assert (
        Child.objects.get(
            first_name=variables["input"]["children"][0]["firstName"]
        ).postal_code
        == ""
    )


def test_submit_children_and_guardian_can_be_done_only_once(guardian_api_client):
    executed = guardian_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    assert "You have already used this mutation." in str(executed["errors"])


CHILDREN_QUERY = """
query Children {
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


def test_children_query_unauthenticated(api_client):
    executed = api_client.execute(CHILDREN_QUERY)

    assert_permission_denied(executed)


def test_children_query_normal_user(snapshot, user_api_client):
    ChildWithGuardianFactory()
    ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)

    executed = user_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)


def test_children_query_staff_user(snapshot, staff_api_client):
    ChildWithGuardianFactory()
    ChildWithGuardianFactory(relationship__guardian__user=staff_api_client.user)

    executed = staff_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)


CHILD_QUERY = """
query Child($id: ID!) {
  child(id: $id) {
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
"""


def test_child_query_unauthenticated(snapshot, api_client):
    child = ChildWithGuardianFactory()
    variables = {"id": to_global_id("ChildNode", child.id)}

    executed = api_client.execute(CHILD_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_child_query(snapshot, user_api_client):
    child = ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)
    variables = {"id": to_global_id("ChildNode", child.id)}

    executed = user_api_client.execute(CHILD_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_child_query_not_own_child(user_api_client):
    child = ChildWithGuardianFactory()
    variables = {"id": to_global_id("ChildNode", child.id)}

    executed = user_api_client.execute(CHILD_QUERY, variables=variables)

    assert executed["data"]["child"] is None


def test_child_query_not_own_child_staff_user(snapshot, staff_api_client):
    child = ChildWithGuardianFactory()
    variables = {"id": to_global_id("ChildNode", child.id)}

    executed = staff_api_client.execute(CHILD_QUERY, variables=variables)

    snapshot.assert_match(executed)


ADD_CHILD_MUTATION = """
mutation AddChild($input: AddChildMutationInput!) {
  addChild(input: $input) {
    child {
      firstName
      lastName
      birthdate
      postalCode
    }
  }
}
"""


ADD_CHILD_VARIABLES = {
    "input": {
        "firstName": "Pekka",
        "lastName": "Perälä",
        "birthdate": "2020-11-11",
        "postalCode": "00820",
        "relationship": {"type": "PARENT"},
    }
}


def test_add_child_mutation(snapshot, guardian_api_client):
    executed = guardian_api_client.execute(
        ADD_CHILD_MUTATION, variables=ADD_CHILD_VARIABLES
    )

    snapshot.assert_match(executed)

    child = Child.objects.last()
    assert_child_matches_data(child, ADD_CHILD_VARIABLES["input"])

    relationship = Relationship.objects.get(
        guardian=guardian_api_client.user.guardian, child=child
    )
    assert_relationship_matches_data(
        relationship, ADD_CHILD_VARIABLES["input"]["relationship"]
    )


def test_add_child_mutation_birthdate_required(guardian_api_client):
    variables = deepcopy(ADD_CHILD_VARIABLES)
    variables["input"].pop("birthdate")
    executed = guardian_api_client.execute(ADD_CHILD_MUTATION, variables=variables)

    assert "birthdate" in str(executed["errors"])
    assert Child.objects.count() == 0


def test_add_child_mutation_postal_code_validation(guardian_api_client):
    variables = deepcopy(ADD_CHILD_VARIABLES)
    variables["input"]["postalCode"] = "1234x"

    executed = guardian_api_client.execute(ADD_CHILD_MUTATION, variables=variables)

    assert "Postal code must be 5 digits" in str(executed["errors"])
    assert Child.objects.count() == 0


def test_add_child_mutation_postal_code_can_be_empty(guardian_api_client):
    variables = deepcopy(ADD_CHILD_VARIABLES)
    variables["input"]["postalCode"] = ""

    guardian_api_client.execute(ADD_CHILD_MUTATION, variables=variables)

    assert (
        Child.objects.get(first_name=variables["input"]["firstName"]).postal_code == ""
    )


def test_add_child_mutation_requires_guardian(user_api_client):
    executed = user_api_client.execute(
        ADD_CHILD_MUTATION, variables=ADD_CHILD_VARIABLES
    )

    assert 'You need to use "SubmitChildrenAndGuardianMutation" first.' in str(
        executed["errors"]
    )
    assert Child.objects.count() == 0


UPDATE_CHILD_MUTATION = """
mutation UpdateChild($input: UpdateChildMutationInput!) {
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


def test_update_child_mutation(snapshot, guardian_api_client):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)

    child.refresh_from_db()
    assert_child_matches_data(child, variables["input"])

    relationship = Relationship.objects.get(
        guardian=guardian_api_client.user.guardian, child=child
    )
    assert_relationship_matches_data(relationship, variables["input"]["relationship"])


def test_update_child_mutation_should_have_no_required_fields(
    snapshot, guardian_api_client
):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    variables = {"input": {"id": to_global_id("ChildNode", child.id)}}

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)


def test_update_child_mutation_wrong_user(user_api_client):
    child = ChildWithGuardianFactory()
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)

    executed = user_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "does not exist" in str(executed["errors"])


def test_update_child_mutation_postal_code_validation(guardian_api_client):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)
    variables["input"]["postalCode"] = "1234x"

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "Postal code must be 5 digits" in str(executed["errors"])


def test_update_child_mutation_postal_code_can_be_empty(guardian_api_client):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user, postal_code="12345",
    )
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child.id)
    variables["input"]["postalCode"] = ""

    guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    child.refresh_from_db()
    assert child.postal_code == ""


DELETE_CHILD_MUTATION = """
mutation DeleteChild($input: DeleteChildMutationInput!) {
  deleteChild(input: $input) {__typename}
}
"""


def test_delete_child_mutation(snapshot, guardian_api_client):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    variables = {"input": {"id": to_global_id("ChildNode", child.id)}}

    executed = guardian_api_client.execute(DELETE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)
    assert Child.objects.count() == 0


def test_delete_child_mutation_wrong_user(snapshot, guardian_api_client):
    child = ChildWithGuardianFactory()
    variables = {"input": {"id": to_global_id("ChildNode", child.id)}}

    executed = guardian_api_client.execute(DELETE_CHILD_MUTATION, variables=variables)

    assert "does not exist" in str(executed["errors"])
    assert Child.objects.count() == 1
