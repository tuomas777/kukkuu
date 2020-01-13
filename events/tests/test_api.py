import pytest
from graphql_relay import to_global_id

from common.tests.utils import assert_permission_denied
from events.factories import EventFactory, OccurrenceFactory


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


EVENTS_QUERY = """
query Events {
  events {
    edges {
      node {
        name
        shortDescription
        description
        createdAt
        updatedAt
        duration
        occurrences {
          edges {
            node {
              time
              venue {
                name
                seatCount
                description
              }
            }
          }
        }
      }
    }
  }
}
"""

EVENT_QUERY = """
query Event($id:ID!) {
  event(id: $id) {
    id
    name
    shortDescription
    description
    createdAt
    updatedAt
    duration
    occurrences{
      edges{
        node{
          time
          venue{
            name
            seatCount
            description
          }
        }
      }
    }
  }
}
"""

OCCURRENCES_QUERY = """
query Occurrences {
  occurrences{
    edges{
      node{
        time
        event{
          name
          duration
          shortDescription
          description
        }
      }
    }
  }
}
"""

OCCURRENCE_QUERY = """
query Occurrence($id: ID!) {
  occurrence(id: $id){
    id
    time
    event{
      name
      shortDescription
      duration
      description
    }
    venue{
      name
      seatCount
      description
    }
  }
}
"""


def test_events_query_unauthenticated(api_client):
    executed = api_client.execute(EVENTS_QUERY)

    assert_permission_denied(executed)


def test_events_query_normal_user(snapshot, user_api_client):
    OccurrenceFactory()

    executed = user_api_client.execute(EVENTS_QUERY)

    snapshot.assert_match(executed)


def test_event_query_unauthenticated(api_client):
    event = EventFactory()
    variables = {"id": to_global_id("EventNode", event.id)}
    executed = api_client.execute(EVENT_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_event_query_normal_user(snapshot, user_api_client):
    event = EventFactory()
    variables = {"id": to_global_id("EventNode", event.id)}
    executed = user_api_client.execute(EVENT_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_occurrences_query_unauthenticated(api_client):
    executed = api_client.execute(OCCURRENCES_QUERY)

    assert_permission_denied(executed)


def test_occurrences_query_normal_user(snapshot, user_api_client):
    OccurrenceFactory()

    executed = user_api_client.execute(OCCURRENCES_QUERY)

    snapshot.assert_match(executed)


def test_occurrence_query_unauthenticated(api_client):
    occurrence = OccurrenceFactory()
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = api_client.execute(OCCURRENCE_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_occurrence_query_normal_user(snapshot, user_api_client):
    occurrence = OccurrenceFactory()
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = user_api_client.execute(OCCURRENCE_QUERY, variables=variables)

    snapshot.assert_match(executed)
