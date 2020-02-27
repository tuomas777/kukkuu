from copy import deepcopy
from datetime import datetime
from typing import Dict

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.utils.translation import activate
from graphql_relay import to_global_id
from parler.utils.context import switch_language

from children.factories import ChildWithGuardianFactory
from common.tests.utils import assert_permission_denied
from events.factories import EnrolmentFactory, EventFactory, OccurrenceFactory
from events.models import Enrolment, Event, Occurrence


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


EVENTS_QUERY = """
query Events {
  events {
    edges {
      node {
        translations{
          name
          description
          shortDescription
          languageCode
        }
        name
        description
        shortDescription
        duration
        image
        participantsPerInvite
        capacityPerOccurrence
        publishedAt
        createdAt
        updatedAt
        occurrences {
          edges {
            node {
              time
              venue {
                translations{
                  name
                  description
                  languageCode
                }
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
    translations{
      name
      shortDescription
      description
      languageCode
    }
    name
    description
    shortDescription
    image
    participantsPerInvite
    capacityPerOccurrence
    publishedAt
    createdAt
    updatedAt
    duration
    occurrences{
      edges{
        node{
          time
          venue{
            translations{
              name
              description
              languageCode
            }
          }
        }
      }
    }
  }
}
"""

OCCURRENCES_QUERY = """
query Occurrences {
  occurrences {
    edges {
      node {
        time
        remainingCapacity
        event {
          translations {
            name
            shortDescription
            description
            languageCode
          }
          image
          participantsPerInvite
          capacityPerOccurrence
          publishedAt
          duration
        }
        venue{
          translations{
            name
            description
            address
            accessibilityInfo
            arrivalInstructions
            additionalInfo
            wwwUrl
            languageCode
          }
        }
      }
    }
  }
}
"""

OCCURRENCES_FILTER_QUERY = """
query Occurrences($date: Date, $time: Time) {
  occurrences(date: $date, time: $time) {
    edges {
      node {
        time
      }
    }
  }
}
"""

OCCURRENCE_QUERY = """
query Occurrence($id: ID!) {
  occurrence(id: $id){
    enrolments{
        edges{
          node{
            child{
              firstName
            }
          }
        }
    }
    time
    remainingCapacity
    event {
      translations {
        name
        shortDescription
        description
        languageCode
      }
      image
      participantsPerInvite
      capacityPerOccurrence
      publishedAt
      duration
    }
    venue{
      translations{
        name
        description
        address
        accessibilityInfo
        arrivalInstructions
        additionalInfo
        wwwUrl
        languageCode
      }
    }
  }
}
"""

ADD_EVENT_MUTATION = """
mutation AddEvent($input: AddEventMutationInput!) {
  addEvent(input: $input) {
    event {
      translations{
        languageCode
        name
        description
        shortDescription
      }
      duration
      image
      participantsPerInvite
      capacityPerOccurrence
      publishedAt
    }
  }
}
"""

ADD_EVENT_VARIABLES = {
    "input": {
        "translations": [
            {
                "name": "Event test",
                "shortDescription": "Short desc",
                "description": "desc",
                "languageCode": "fi",
            }
        ],
        "duration": 1000,
        "participantsPerInvite": "family",
        "capacityPerOccurrence": 30,
    }
}

UPDATE_EVENT_MUTATION = """
mutation UpdateEvent($input: UpdateEventMutationInput!) {
  updateEvent(input: $input) {
    event {
      translations{
        name
        shortDescription
        description
        languageCode
      }
      participantsPerInvite
      capacityPerOccurrence
      duration
      occurrences{
        edges{
          node{
            time
          }
        }
      }
    }
  }
}
"""

UPDATE_EVENT_VARIABLES = {
    "input": {
        "id": "",
        "translations": [
            {
                "name": "Event test in suomi",
                "shortDescription": "Short desc",
                "description": "desc",
                "languageCode": "sv",
            }
        ],
        "duration": 1000,
        "participantsPerInvite": "family",
        "capacityPerOccurrence": 30,
    }
}

PUBLISH_EVENT_MUTATION = """
mutation PublishEvent($input: PublishEventMutationInput!) {
  publishEvent(input: $input) {
    event {
      publishedAt
    }
  }
}
"""

PUBLISH_EVENT_VARIABLES = {"input": {"id": ""}}

DELETE_EVENT_MUTATION = """
mutation DeleteEvent($input: DeleteEventMutationInput!) {
  deleteEvent(input: $input) {
    __typename
  }
}
"""

ADD_OCCURRENCE_MUTATION = """
mutation AddOccurrence($input: AddOccurrenceMutationInput!) {
  addOccurrence(input: $input) {
    occurrence{
      event{
        createdAt
      }
      venue {
        createdAt
      }
      time
    }
  }
}

"""

ADD_OCCURRENCE_VARIABLES = {
    "input": {"eventId": "", "venueId": "", "time": "1986-12-12T16:40:48+00:00"}
}

UPDATE_OCCURRENCE_MUTATION = """
mutation UpdateOccurrence($input: UpdateOccurrenceMutationInput!) {
  updateOccurrence(input: $input) {
    occurrence{
      event{
        createdAt
      }
      venue {
        createdAt
      }
      time
    }
  }
}

"""

UPDATE_OCCURRENCE_VARIABLES = {
    "input": {
        "id": "",
        "eventId": "",
        "venueId": "",
        "time": "1986-12-12T16:40:48+00:00",
    }
}

DELETE_OCCURRENCE_MUTATION = """
mutation DeleteOccurrence($input: DeleteOccurrenceMutationInput!) {
  deleteOccurrence(input: $input) {
    __typename
  }
}

"""

ENROL_OCCURRENCE_MUTATION = """
mutation EnrolOccurrence($input: EnrolOccurrenceMutationInput!) {
  enrolOccurrence(input: $input) {
    enrolment{
      child{
        firstName
      }
      occurrence {
        time
      }
      createdAt
    }
  }
}

"""

ENROL_OCCURRENCE_VARIABLES = {"input": {"occurrenceId": "", "childId": ""}}

UNENROL_OCCURRENCE_MUTATION = """
mutation UnenrolOccurrence($input: UnenrolOccurrenceMutationInput!) {
  unenrolOccurrence(input: $input) {
    __typename
  }
}

"""


def test_events_query_unauthenticated(api_client):
    executed = api_client.execute(EVENTS_QUERY)

    assert_permission_denied(executed)


def test_events_query_normal_user(snapshot, user_api_client, event):
    executed = user_api_client.execute(EVENTS_QUERY)

    snapshot.assert_match(executed)


def test_event_query_unauthenticated(api_client, event):
    variables = {"id": to_global_id("EventNode", event.id)}
    executed = api_client.execute(EVENT_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_event_query_normal_user(snapshot, user_api_client, event):
    variables = {"id": to_global_id("EventNode", event.id)}
    executed = user_api_client.execute(EVENT_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_occurrences_query_unauthenticated(api_client):
    executed = api_client.execute(OCCURRENCES_QUERY)

    assert_permission_denied(executed)


def test_occurrences_query_normal_user(snapshot, user_api_client, occurrence):
    executed = user_api_client.execute(OCCURRENCES_QUERY)

    snapshot.assert_match(executed)


def test_occurrence_query_unauthenticated(api_client, occurrence):
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = api_client.execute(OCCURRENCE_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_occurrence_query_normal_user(snapshot, user_api_client, occurrence):
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = user_api_client.execute(OCCURRENCE_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_add_event_permission_denied(api_client, user_api_client):
    executed = api_client.execute(ADD_EVENT_MUTATION, variables=ADD_EVENT_VARIABLES)
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ADD_EVENT_MUTATION, variables=ADD_EVENT_VARIABLES
    )
    assert_permission_denied(executed)


def test_add_event_staff_user(snapshot, staff_api_client):
    executed = staff_api_client.execute(
        ADD_EVENT_MUTATION, variables=ADD_EVENT_VARIABLES
    )
    snapshot.assert_match(executed)


def test_add_occurrence_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=ADD_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)


def test_add_occurrence_staff_user(snapshot, staff_api_client, event, venue):
    occurrence_variables = deepcopy(ADD_OCCURRENCE_VARIABLES)
    occurrence_variables["input"]["eventId"] = to_global_id("EventNode", event.id)
    occurrence_variables["input"]["venueId"] = to_global_id("VenueNode", venue.id)
    executed = staff_api_client.execute(
        ADD_OCCURRENCE_MUTATION, variables=occurrence_variables
    )
    snapshot.assert_match(executed)


def test_update_occurrence_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        UPDATE_OCCURRENCE_MUTATION, variables=UPDATE_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        UPDATE_OCCURRENCE_MUTATION, variables=UPDATE_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_occurrence_staff_user(snapshot, staff_api_client, occurrence):
    occurrence_variables = deepcopy(UPDATE_OCCURRENCE_VARIABLES)
    occurrence_variables["input"]["id"] = to_global_id("OccurrenceNode", occurrence.id)
    occurrence_variables["input"]["eventId"] = to_global_id(
        "EventNode", occurrence.event.id
    )
    occurrence_variables["input"]["venueId"] = to_global_id(
        "VenueNode", occurrence.venue.id
    )
    executed = staff_api_client.execute(
        UPDATE_OCCURRENCE_MUTATION, variables=occurrence_variables
    )
    snapshot.assert_match(executed)


def test_delete_occurrence_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        DELETE_OCCURRENCE_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        DELETE_OCCURRENCE_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)


def test_delete_occurrence_staff_user(staff_api_client, occurrence):
    staff_api_client.execute(
        DELETE_OCCURRENCE_MUTATION,
        variables={"input": {"id": to_global_id("OccurrenceNode", occurrence.id)}},
    )
    assert Occurrence.objects.count() == 0


def test_update_event_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=UPDATE_EVENT_VARIABLES
    )
    assert_permission_denied(executed)


def test_update_event_staff_user(snapshot, staff_api_client, event):
    event_variables = deepcopy(UPDATE_EVENT_VARIABLES)
    event_variables["input"]["id"] = to_global_id("EventNode", event.id)
    executed = staff_api_client.execute(
        UPDATE_EVENT_MUTATION, variables=event_variables
    )
    snapshot.assert_match(executed)


def test_delete_event_permission_denied(api_client, user_api_client):
    executed = api_client.execute(
        DELETE_EVENT_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)

    executed = user_api_client.execute(
        DELETE_EVENT_MUTATION, variables={"input": {"id": ""}}
    )
    assert_permission_denied(executed)


def test_delete_event_staff_user(staff_api_client, event):
    staff_api_client.execute(
        DELETE_EVENT_MUTATION,
        variables={"input": {"id": to_global_id("EventNode", event.id)}},
    )
    assert Event.objects.count() == 0


def test_update_event_translations(staff_api_client, event):
    event = EventFactory()
    assert event.translations.count() == 1
    event_variables = deepcopy(UPDATE_EVENT_VARIABLES)
    event_variables["input"]["id"] = to_global_id("EventNode", event.id)

    # Test add translation
    new_translation: Dict[str, (list, str)] = {
        "name": "Event name",
        "description": "Event description",
        "shortDescription": "Event short description",
        "languageCode": "sv",
    }
    event_variables["input"]["translations"].append(new_translation)
    staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=event_variables)
    assert event.has_translation(new_translation["languageCode"])

    # Test delete translation
    event_variables["input"]["deleteTranslations"] = [new_translation["languageCode"]]
    staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=event_variables)
    assert not event.has_translation(new_translation["languageCode"])

    # Test invalid translation
    new_translation["languageCode"] = "foo"
    staff_api_client.execute(UPDATE_EVENT_MUTATION, variables=event_variables)
    assert not event.has_translation(new_translation["languageCode"])


def test_upload_image_to_event(staff_api_client, snapshot):
    add_event_variables = deepcopy(ADD_EVENT_VARIABLES)
    # noinspection PyTypeChecker
    add_event_variables["input"]["image"] = SimpleUploadedFile(
        "sample.jpg", content=None, content_type="image/jpeg"
    )

    staff_api_client.execute(ADD_EVENT_MUTATION, variables=add_event_variables)
    assert Event.objects.count() == 1
    event = Event.objects.first()
    assert event.image


def test_staff_publish_event(snapshot, staff_api_client, event):
    assert not event.is_published()
    event_variables = deepcopy(PUBLISH_EVENT_VARIABLES)
    event_variables["input"]["id"] = to_global_id("EventNode", event.id)
    executed = staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=event_variables
    )
    snapshot.assert_match(executed)

    executed = staff_api_client.execute(
        PUBLISH_EVENT_MUTATION, variables=event_variables
    )
    assert "Event is already published" in str(executed["errors"])


def test_enrol_occurrence(api_client, guardian_api_client, snapshot, occurrence):
    non_authen_executed = api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=ENROL_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(non_authen_executed)

    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )

    enrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    enrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    enrolment_variables["input"]["childId"] = to_global_id("ChildNode", child.id)

    executed = guardian_api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=enrolment_variables
    )
    snapshot.assert_match(executed)


def test_already_enroled_occurrence(guardian_api_client, snapshot, occurrence):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    EnrolmentFactory(child=child, occurrence=occurrence)

    enrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    enrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    enrolment_variables["input"]["childId"] = to_global_id("ChildNode", child.id)

    executed = guardian_api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=enrolment_variables
    )

    assert "Child already joined this event" in str(executed["errors"])


def test_enrol_occurrence_not_allowed(guardian_api_client, snapshot, occurrence):
    random_child = ChildWithGuardianFactory()
    enrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    enrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    enrolment_variables["input"]["childId"] = to_global_id("ChildNode", random_child.id)

    executed = guardian_api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=enrolment_variables
    )
    assert "does not exist" in str(executed["errors"])


def test_unenrol_occurrence(api_client, user_api_client, snapshot, occurrence):
    non_authen_executed = api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=ENROL_OCCURRENCE_VARIABLES
    )
    assert_permission_denied(non_authen_executed)

    child = ChildWithGuardianFactory(relationship__guardian__user=user_api_client.user)
    EnrolmentFactory(occurrence=occurrence, child=child)

    random_child = ChildWithGuardianFactory()
    EnrolmentFactory(occurrence=occurrence, child=random_child)
    assert Enrolment.objects.count() == 2
    assert child.occurrences.count() == 1
    assert random_child.occurrences.count() == 1

    unenrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    unenrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    unenrolment_variables["input"]["childId"] = to_global_id(
        "ChildNode", random_child.id
    )

    executed = user_api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=unenrolment_variables
    )
    assert "does not exist" in str(executed["errors"])
    assert Enrolment.objects.count() == 2
    assert child.occurrences.count() == 1
    assert random_child.occurrences.count() == 1

    unenrolment_variables["input"]["childId"] = to_global_id("ChildNode", child.id)
    user_api_client.execute(
        UNENROL_OCCURRENCE_MUTATION, variables=unenrolment_variables
    )
    assert Enrolment.objects.count() == 1
    assert child.occurrences.count() == 0
    assert random_child.occurrences.count() == 1


def test_maximum_enrolment(guardian_api_client, occurrence):
    max_capactity = occurrence.event.capacity_per_occurrence
    children = ChildWithGuardianFactory.create_batch(max_capactity)
    for child in children:
        EnrolmentFactory(occurrence=occurrence, child=child)
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )

    enrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    enrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    enrolment_variables["input"]["childId"] = to_global_id("ChildNode", child.id)

    executed = guardian_api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=enrolment_variables
    )
    assert "Maximum enrolments created" in str(executed["errors"])


def test_invalid_occurrence_enrolment(guardian_api_client):
    occurrence = OccurrenceFactory(
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.now().tzinfo)
    )
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    enrolment_variables = deepcopy(ENROL_OCCURRENCE_VARIABLES)
    enrolment_variables["input"]["occurrenceId"] = to_global_id(
        "OccurrenceNode", occurrence.id
    )
    enrolment_variables["input"]["childId"] = to_global_id("ChildNode", child.id)
    executed = guardian_api_client.execute(
        ENROL_OCCURRENCE_MUTATION, variables=enrolment_variables
    )
    assert "Cannot join occurrence in the past" in str(executed["errors"])


def test_normal_translation_fields(snapshot, user_api_client, event):
    variables = {"id": to_global_id("EventNode", event.id)}
    for code in settings.PARLER_SUPPORTED_LANGUAGE_CODES:
        new_translation = "{} Translation".format(code)
        with switch_language(event, code):
            event.name = new_translation
            event.save()
        activate(code)
        executed = user_api_client.execute(EVENT_QUERY, variables=variables)
        translation = [
            trans
            for trans in executed["data"]["event"]["translations"]
            if trans["languageCode"] == code.upper()
        ][0]["name"]
        assert executed["data"]["event"]["name"] == translation


def test_occurrences_filter_by_date(user_api_client, snapshot):
    OccurrenceFactory(time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.now().tzinfo))
    OccurrenceFactory(time=datetime(1970, 1, 2, 0, 0, 0, tzinfo=timezone.now().tzinfo))
    variables = {"date": "1970-01-02"}
    executed = user_api_client.execute(OCCURRENCES_FILTER_QUERY, variables=variables)

    assert len(executed["data"]["occurrences"]["edges"]) == 1
    OccurrenceFactory(time=datetime(1970, 1, 2, 0, 0, 0, tzinfo=timezone.now().tzinfo))
    executed = user_api_client.execute(OCCURRENCES_FILTER_QUERY, variables=variables)
    assert len(executed["data"]["occurrences"]["edges"]) == 2
    snapshot.assert_match(executed)


def test_occurrences_filter_by_time(user_api_client, snapshot):
    for i in range(10, 12):
        OccurrenceFactory(
            time=datetime(1970, 1, 1, i, 0, 0, tzinfo=timezone.now().tzinfo)
        )
        OccurrenceFactory(
            time=datetime(1970, 1, 2, i + 1, 0, 0, tzinfo=timezone.now().tzinfo)
        )
    OccurrenceFactory(time=datetime(1970, 1, 1, 13, 0, 0, tzinfo=timezone.now().tzinfo))
    variables_1 = {"time": "12:00:00"}
    variables_2 = {"time": "14:00:00+02:00"}
    variables_3 = {"time": "11:00:00+00:00"}

    executed = user_api_client.execute(OCCURRENCES_FILTER_QUERY, variables=variables_1)
    assert len(executed["data"]["occurrences"]["edges"]) == 1
    executed = user_api_client.execute(OCCURRENCES_FILTER_QUERY, variables=variables_2)
    assert len(executed["data"]["occurrences"]["edges"]) == 1
    executed = user_api_client.execute(OCCURRENCES_FILTER_QUERY, variables=variables_3)
    assert len(executed["data"]["occurrences"]["edges"]) == 2
    snapshot.assert_match(executed)


def test_occurrence_available_capacity(user_api_client, snapshot, occurrence):
    max_capacity = occurrence.event.capacity_per_occurrence
    EnrolmentFactory.create_batch(3, occurrence=occurrence)
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = user_api_client.execute(OCCURRENCE_QUERY, variables=variables)
    assert executed["data"]["occurrence"]["remainingCapacity"] == max_capacity - 3
    e = EnrolmentFactory(occurrence=occurrence)
    executed = user_api_client.execute(OCCURRENCE_QUERY, variables=variables)
    assert executed["data"]["occurrence"]["remainingCapacity"] == max_capacity - 4
    e.delete()
    executed = user_api_client.execute(OCCURRENCE_QUERY, variables=variables)
    assert executed["data"]["occurrence"]["remainingCapacity"] == max_capacity - 3
    snapshot.assert_match(executed)


def test_enrolment_visibility(guardian_api_client, snapshot, occurrence):
    EnrolmentFactory.create_batch(3, occurrence=occurrence)
    child = ChildWithGuardianFactory(
        relationship__guardian__user=guardian_api_client.user
    )
    EnrolmentFactory(child=child, occurrence=occurrence)
    variables = {"id": to_global_id("OccurrenceNode", occurrence.id)}
    executed = guardian_api_client.execute(OCCURRENCE_QUERY, variables=variables)
    assert len(executed["data"]["occurrence"]["enrolments"]["edges"]) == 1
    snapshot.assert_match(executed)
