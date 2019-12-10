import pytest

from children.tests.test_api import assert_permission_denied
from users.factories import GuardianFactory


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
