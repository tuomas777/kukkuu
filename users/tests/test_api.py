import pytest

from users.factories import GuardianFactory

GUARDIANS_QUERY = """
query getGuardians {
  guardians {
    edges {
      node {
        firstName
        lastName
        phoneNumber
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


@pytest.mark.django_db
def test_guardians_query_unauthenticated(api_client):
    executed = api_client.execute(GUARDIANS_QUERY)

    # TODO add better check when we have error codes
    assert "errors" in executed


@pytest.mark.django_db
def test_guardians_query_normal_user(snapshot, user_api_client):
    GuardianFactory(relationships__count=1)
    GuardianFactory(user=user_api_client.user, relationships__count=1)

    executed = user_api_client.execute(GUARDIANS_QUERY)

    snapshot.assert_match(executed)


@pytest.mark.django_db
def test_guardians_query_staff_user(snapshot, staff_api_client):
    GuardianFactory(relationships__count=1)
    GuardianFactory(user=staff_api_client.user, relationships__count=1)

    executed = staff_api_client.execute(GUARDIANS_QUERY)

    snapshot.assert_match(executed)
