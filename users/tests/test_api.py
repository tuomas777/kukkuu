import pytest

from children.tests.test_api import (
    assert_guardian_matches_data,
    assert_permission_denied,
)
from users.factories import GuardianFactory
from users.models import Guardian


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


GUARDIANS_QUERY = """
query Guardians {
  guardians {
    edges {
      node {
        firstName
        lastName
        phoneNumber
        email
        relationships {
          edges {
            node {
              type
              child {
                firstName
                lastName
                birthdate
              }
            }
          }
        }
      }
    }
  }
}
"""


def test_guardians_query_unauthenticated(api_client):
    executed = api_client.execute(GUARDIANS_QUERY)

    assert_permission_denied(executed)


def test_guardians_query_normal_user(snapshot, user_api_client):
    GuardianFactory(relationships__count=1)
    GuardianFactory(user=user_api_client.user, relationships__count=1)

    executed = user_api_client.execute(GUARDIANS_QUERY)

    snapshot.assert_match(executed)


def test_guardians_query_staff_user(snapshot, staff_api_client):
    GuardianFactory(relationships__count=1)
    GuardianFactory(user=staff_api_client.user, relationships__count=1)

    executed = staff_api_client.execute(GUARDIANS_QUERY)

    snapshot.assert_match(executed)


MY_PROFILE_QUERY = """
query MyProfile {
  myProfile {
    firstName
    lastName
    phoneNumber
    email
    relationships {
      edges {
        node {
          type
          child {
            firstName
            lastName
            birthdate
            postalCode
          }
        }
      }
    }
  }
}
"""

MY_ADMIN_PROFILE_QUERY = """
query MyAdminProfle{
  myAdminProfile{
    isProjectAdmin
  }
}
"""


def test_my_profile_query_unauthenticated(api_client):
    GuardianFactory()

    executed = api_client.execute(MY_PROFILE_QUERY)

    assert executed["data"]["myProfile"] is None
    assert_permission_denied(executed)


def test_my_profile_query(snapshot, user_api_client):
    GuardianFactory()
    GuardianFactory(user=user_api_client.user, relationships__count=1)
    GuardianFactory(relationships__count=1)

    executed = user_api_client.execute(MY_PROFILE_QUERY)

    snapshot.assert_match(executed)


def test_my_profile_no_profile(snapshot, staff_api_client):
    GuardianFactory()

    executed = staff_api_client.execute(MY_PROFILE_QUERY)

    snapshot.assert_match(executed)


UPDATE_MY_PROFILE_MUTATION = """
mutation UpdateMyProfile($input: UpdateMyProfileMutationInput!) {
  updateMyProfile(input: $input) {
    myProfile {
      firstName
      lastName
      phoneNumber
      language
    }
  }
}
"""

UPDATE_MY_PROFILE_VARIABLES = {
    "input": {
        "firstName": "Updated First Name",
        "lastName": "Updated Last Name",
        "phoneNumber": "Updated phone number",
        "language": "EN",
    }
}


def test_update_my_profile_mutation_unauthenticated(api_client):
    executed = api_client.execute(
        UPDATE_MY_PROFILE_MUTATION, variables=UPDATE_MY_PROFILE_VARIABLES
    )

    assert_permission_denied(executed)


def test_update_my_profile_mutation(snapshot, user_api_client):
    GuardianFactory(user=user_api_client.user, language="fi")

    executed = user_api_client.execute(
        UPDATE_MY_PROFILE_MUTATION, variables=UPDATE_MY_PROFILE_VARIABLES
    )

    snapshot.assert_match(executed)
    guardian = Guardian.objects.get(user=user_api_client.user)
    assert_guardian_matches_data(guardian, UPDATE_MY_PROFILE_VARIABLES["input"])


def test_my_admin_profile_unauthenticated(api_client):
    executed = api_client.execute(MY_ADMIN_PROFILE_QUERY)
    assert_permission_denied(executed)


def test_my_admin_profile_authenticated(user_api_client, staff_api_client):
    executed = user_api_client.execute(MY_ADMIN_PROFILE_QUERY)
    assert not executed["data"]["myAdminProfile"]["isProjectAdmin"]
    executed = staff_api_client.execute(MY_ADMIN_PROFILE_QUERY)
    assert executed["data"]["myAdminProfile"]["isProjectAdmin"]
