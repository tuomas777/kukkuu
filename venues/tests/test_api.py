import pytest
from graphql_relay import to_global_id

from common.tests.utils import assert_permission_denied
from events.factories import OccurrenceFactory


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


VENUES_QUERY = """
query Venues {
  venues {
    edges {
      node {
        name,
        description,
        seatCount,
        occurrences {
          edges {
            node {
              time,
              event{
                name,
                description,
                shortDescription,
                duration
              }
            }
          }
        }
      }
    }
  }
}

"""

VENUE_QUERY = """
query Venue($id: ID!) {
  venue(id: $id){
    name,
    seatCount,
    description,
    occurrences{
      edges{
        node{
          time,
          event{
            name,
            description,
            shortDescription,
            duration
          }
        }
      }
    }
  }
}
"""


def test_venues_query_unauthenticated(api_client):
    executed = api_client.execute(VENUES_QUERY)

    assert_permission_denied(executed)


def test_venues_query_normal_user(snapshot, user_api_client):
    OccurrenceFactory()

    executed = user_api_client.execute(VENUES_QUERY)

    snapshot.assert_match(executed)


def test_venue_query_unauthenticated(api_client):
    occurrence = OccurrenceFactory()
    venue = occurrence.venue
    variables = {"id": to_global_id("VenueNode", venue.id)}
    executed = api_client.execute(VENUE_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_venue_query_normal_user(snapshot, user_api_client):
    occurrence = OccurrenceFactory()
    venue = occurrence.venue
    variables = {"id": to_global_id("VenueNode", venue.id)}
    executed = user_api_client.execute(VENUE_QUERY, variables=variables)

    snapshot.assert_match(executed)
