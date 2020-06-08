from copy import deepcopy
from datetime import date, datetime, timedelta

import pytest
import pytz
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime, now
from graphene.utils.str_converters import to_snake_case
from graphql_relay import to_global_id
from projects.factories import ProjectFactory

from children.factories import ChildWithGuardianFactory
from common.tests.utils import assert_match_error_code, assert_permission_denied
from events.factories import EnrolmentFactory, EventFactory, OccurrenceFactory
from kukkuu.consts import (
    API_USAGE_ERROR,
    DATA_VALIDATION_ERROR,
    GENERAL_ERROR,
    INVALID_EMAIL_FORMAT_ERROR,
    MAX_NUMBER_OF_CHILDREN_PER_GUARDIAN_ERROR,
    OBJECT_DOES_NOT_EXIST_ERROR,
)
from users.factories import GuardianFactory
from users.models import Guardian

from ..models import Child, Relationship


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


@pytest.fixture(params=("1234x", ""))
def invalid_postal_code(request):
    return request.param


@pytest.fixture(params=[0, 1])
def illegal_birthdate(request):
    # these dates cannot be set to params directly because now() would not be
    # the faked one
    return (
        date(2019, 10, 10),  # wrong year
        localtime(now()).date() + timedelta(days=1),  # in the future
    )[request.param]


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
    for field_name in ("firstName", "lastName", "phoneNumber", "email"):
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


def test_submit_children_and_guardian_with_email(snapshot, user_api_client):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["guardian"]["email"] = "updated_email@example.com"

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    snapshot.assert_match(executed)

    guardian = Guardian.objects.last()
    assert_guardian_matches_data(guardian, variables["input"]["guardian"])


def test_submit_children_and_guardian_one_child_required(snapshot, user_api_client):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"] = []

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert_match_error_code(executed, API_USAGE_ERROR)
    assert "At least one child is required." in str(executed["errors"])


def test_submit_children_and_guardian_postal_code_validation(
    user_api_client, invalid_postal_code
):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"][0]["postalCode"] = invalid_postal_code

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert_match_error_code(executed, DATA_VALIDATION_ERROR)
    assert "Postal code must be 5 digits" in str(executed["errors"])


def test_submit_children_and_guardian_birthdate_validation(
    user_api_client, illegal_birthdate
):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"][0]["birthdate"] = illegal_birthdate

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert_match_error_code(executed, DATA_VALIDATION_ERROR)
    assert "Illegal birthdate." in str(executed["errors"])


def test_submit_children_and_guardian_can_be_done_only_once(guardian_api_client):
    executed = guardian_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION,
        variables=SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES,
    )

    assert_match_error_code(executed, API_USAGE_ERROR)
    assert "You have already used this mutation." in str(executed["errors"])


def test_submit_children_and_guardian_children_limit(user_api_client, settings):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["children"] = [
        variables["input"]["children"][0]
        for _ in range(settings.KUKKUU_MAX_NUM_OF_CHILDREN_PER_GUARDIAN + 1)
    ]

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables,
    )

    assert_match_error_code(executed, MAX_NUMBER_OF_CHILDREN_PER_GUARDIAN_ERROR)
    assert "Too many children." in str(executed["errors"])


@pytest.mark.parametrize("guardian_email", ["INVALID_EMAIL", "", None])
def test_submit_children_and_guardian_email_validation(user_api_client, guardian_email):
    variables = deepcopy(SUBMIT_CHILDREN_AND_GUARDIAN_VARIABLES)
    variables["input"]["guardian"]["email"] = guardian_email

    executed = user_api_client.execute(
        SUBMIT_CHILDREN_AND_GUARDIAN_MUTATION, variables=variables
    )

    assert_match_error_code(executed, INVALID_EMAIL_FORMAT_ERROR)


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


def test_children_query_normal_user(snapshot, user_api_client, project):
    ChildWithGuardianFactory(
        relationship__guardian__user=user_api_client.user, project=project
    )

    executed = user_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)


def test_children_query_project_user(
    snapshot, project_user_api_client, project, another_project
):
    ChildWithGuardianFactory(
        first_name="Same project", last_name="Should be returned 1/1", project=project
    )
    ChildWithGuardianFactory(
        first_name="Another project",
        last_name="Should NOT be returned",
        project=another_project,
    )

    executed = project_user_api_client.execute(CHILDREN_QUERY)

    snapshot.assert_match(executed)


def test_children_query_project_user_and_guardian(
    snapshot, project_user_api_client, project, another_project
):
    guardian = GuardianFactory(user=project_user_api_client.user)

    ChildWithGuardianFactory(
        first_name="Own child same project",
        last_name="Should be returned 1/3",
        project=project,
        relationship__guardian=guardian,
    )
    ChildWithGuardianFactory(
        first_name="Own child another project",
        last_name="Should be returned 2/3",
        project=project,
        relationship__guardian=guardian,
    )
    ChildWithGuardianFactory(
        first_name="Not own child same project",
        last_name="Should be returned 3/3",
        project=project,
    )
    ChildWithGuardianFactory(
        first_name="Not own child another project",
        last_name="Should NOT be returned",
        project=another_project,
    )

    executed = project_user_api_client.execute(CHILDREN_QUERY)

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

CHILD_EVENTS_QUERY = """
query Child($id: ID!) {
  child(id: $id) {
    availableEvents{
      edges{
        node{
          createdAt
          occurrences{
            edges{
              node{
                remainingCapacity
              }
            }
          }
        }
      }
    }
    pastEvents{
      edges{
        node{
          createdAt
          occurrences{
            edges{
              node{
                remainingCapacity
              }
            }
          }
        }
      }
    }
    occurrences {
      edges {
        node {
          time
        }
      }
    }
  }
}
"""


def test_child_query_unauthenticated(snapshot, api_client, child_with_random_guardian):
    variables = {"id": to_global_id("ChildNode", child_with_random_guardian.id)}

    executed = api_client.execute(CHILD_QUERY, variables=variables)

    assert_permission_denied(executed)


def test_child_query(snapshot, user_api_client, project):
    child = ChildWithGuardianFactory(
        relationship__guardian__user=user_api_client.user, project=project
    )
    variables = {"id": to_global_id("ChildNode", child.id)}

    executed = user_api_client.execute(CHILD_QUERY, variables=variables)

    snapshot.assert_match(executed)


def test_child_query_not_own_child(user_api_client, child_with_random_guardian):
    variables = {"id": to_global_id("ChildNode", child_with_random_guardian.id)}

    executed = user_api_client.execute(CHILD_QUERY, variables=variables)

    assert executed["data"]["child"] is None


def test_child_query_not_own_child_project_user(
    snapshot, project_user_api_client, child_with_random_guardian
):
    variables = {"id": to_global_id("ChildNode", child_with_random_guardian.id)}

    executed = project_user_api_client.execute(CHILD_QUERY, variables=variables)

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

    # GraphQL input error for missing required fields
    assert_match_error_code(executed, GENERAL_ERROR)
    assert "birthdate" in str(executed["errors"])
    assert Child.objects.count() == 0


def test_add_child_mutation_postal_code_validation(
    guardian_api_client, invalid_postal_code
):
    variables = deepcopy(ADD_CHILD_VARIABLES)
    variables["input"]["postalCode"] = invalid_postal_code

    executed = guardian_api_client.execute(ADD_CHILD_MUTATION, variables=variables)

    assert_match_error_code(executed, DATA_VALIDATION_ERROR)
    assert "Postal code must be 5 digits" in str(executed["errors"])
    assert Child.objects.count() == 0


def test_add_child_mutation_birthdate_validation(
    guardian_api_client, illegal_birthdate
):
    variables = deepcopy(ADD_CHILD_VARIABLES)
    variables["input"]["birthdate"] = illegal_birthdate

    executed = guardian_api_client.execute(ADD_CHILD_MUTATION, variables=variables)
    assert_match_error_code(executed, DATA_VALIDATION_ERROR)
    assert "Illegal birthdate." in str(executed["errors"])


def test_add_child_mutation_requires_guardian(user_api_client):
    executed = user_api_client.execute(
        ADD_CHILD_MUTATION, variables=ADD_CHILD_VARIABLES
    )
    assert_match_error_code(executed, API_USAGE_ERROR)
    assert 'You need to use "SubmitChildrenAndGuardianMutation" first.' in str(
        executed["errors"]
    )
    assert Child.objects.count() == 0


def test_add_child_mutation_children_limit(guardian_api_client, settings, project):
    ChildWithGuardianFactory.create_batch(
        settings.KUKKUU_MAX_NUM_OF_CHILDREN_PER_GUARDIAN,
        relationship__guardian=guardian_api_client.user.guardian,
        project=project,
    )

    executed = guardian_api_client.execute(
        ADD_CHILD_MUTATION, variables=ADD_CHILD_VARIABLES
    )

    assert_match_error_code(executed, MAX_NUMBER_OF_CHILDREN_PER_GUARDIAN_ERROR)


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


def test_update_child_mutation(snapshot, guardian_api_client, child_with_user_guardian):
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child_with_user_guardian.id)

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)

    child_with_user_guardian.refresh_from_db()
    assert_child_matches_data(child_with_user_guardian, variables["input"])

    relationship = Relationship.objects.get(
        guardian=guardian_api_client.user.guardian, child=child_with_user_guardian
    )
    assert_relationship_matches_data(relationship, variables["input"]["relationship"])


def test_update_child_mutation_should_have_no_required_fields(
    snapshot, guardian_api_client, child_with_user_guardian
):
    variables = {
        "input": {"id": to_global_id("ChildNode", child_with_user_guardian.id)}
    }

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)


def test_update_child_mutation_wrong_user(user_api_client, child_with_random_guardian):
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child_with_random_guardian.id)

    executed = user_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert_match_error_code(executed, OBJECT_DOES_NOT_EXIST_ERROR)


def test_update_child_mutation_postal_code_validation(
    guardian_api_client, invalid_postal_code, child_with_user_guardian
):
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child_with_user_guardian.id)
    variables["input"]["postalCode"] = invalid_postal_code

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "Postal code must be 5 digits" in str(executed["errors"])


def test_update_child_mutation_birthdate_validation(
    guardian_api_client, illegal_birthdate, child_with_user_guardian
):
    variables = deepcopy(UPDATE_CHILD_VARIABLES)
    variables["input"]["id"] = to_global_id("ChildNode", child_with_user_guardian.id)
    variables["input"]["birthdate"] = illegal_birthdate

    executed = guardian_api_client.execute(UPDATE_CHILD_MUTATION, variables=variables)

    assert "Illegal birthdate." in str(executed["errors"])


DELETE_CHILD_MUTATION = """
mutation DeleteChild($input: DeleteChildMutationInput!) {
  deleteChild(input: $input) {__typename}
}
"""


def test_delete_child_mutation(snapshot, guardian_api_client, child_with_user_guardian):
    variables = {
        "input": {"id": to_global_id("ChildNode", child_with_user_guardian.id)}
    }

    executed = guardian_api_client.execute(DELETE_CHILD_MUTATION, variables=variables)

    snapshot.assert_match(executed)
    assert Child.objects.count() == 0


def test_delete_child_mutation_wrong_user(
    snapshot, guardian_api_client, child_with_random_guardian
):
    variables = {
        "input": {"id": to_global_id("ChildNode", child_with_random_guardian.id)}
    }

    executed = guardian_api_client.execute(DELETE_CHILD_MUTATION, variables=variables)

    assert_match_error_code(executed, OBJECT_DOES_NOT_EXIST_ERROR)
    assert Child.objects.count() == 1


def test_get_available_events(
    snapshot,
    guardian_api_client,
    unpublished_event,
    child_with_user_guardian,
    project,
    venue,
):
    variables = {"id": to_global_id("ChildNode", child_with_user_guardian.id)}
    next_project = ProjectFactory(year=2021)
    # Unpublished occurrences
    OccurrenceFactory(time=timezone.now(), event=unpublished_event, venue=venue)

    # Published occurrences
    occurrence = OccurrenceFactory(
        time=timezone.now(),
        event__published_at=timezone.now(),
        event__project=project,
        venue=venue,
    )
    OccurrenceFactory(
        time=timezone.now(),
        event__published_at=timezone.now(),
        event__project=project,
        venue=venue,
    )

    # Published occurrence but from another project
    OccurrenceFactory(
        time=timezone.now(),
        event__published_at=timezone.now(),
        event__project=next_project,
        venue=venue,
    )

    # Past occurrences
    OccurrenceFactory.create_batch(
        3,
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        event__project=project,
        venue=venue,
    )

    EnrolmentFactory(child=child_with_user_guardian, occurrence=occurrence)
    executed = guardian_api_client.execute(CHILD_EVENTS_QUERY, variables=variables)
    # Should only return available events from current project
    assert len(executed["data"]["child"]["availableEvents"]["edges"]) == 1
    snapshot.assert_match(executed)


def test_get_past_events(
    snapshot, guardian_api_client, child_with_user_guardian, project, venue
):
    variables = {"id": to_global_id("ChildNode", child_with_user_guardian.id)}

    next_project = ProjectFactory(year=2021)

    # Unpublished occurrences
    OccurrenceFactory.create_batch(
        2, time=timezone.now(), event=EventFactory(project=project), venue=venue
    )

    # Published occurrences in the past
    event = EventFactory(published_at=timezone.now(), project=project)
    past_occurrence_1 = OccurrenceFactory(
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        event=event,
        venue=venue,
    )

    OccurrenceFactory(
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        event__published_at=timezone.now(),
        event__project=project,
        venue=venue,
    )
    # Past occurrence but from another project
    OccurrenceFactory(
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        event__published_at=timezone.now(),
        event__project=next_project,
        venue=venue,
    )

    # Recent published occurrence
    OccurrenceFactory(time=timezone.now(), event=event, venue=venue)

    # Unpublished occurrences in the past
    OccurrenceFactory.create_batch(
        3,
        time=datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.timezone(settings.TIME_ZONE)),
        event__project=project,
        venue=venue,
    )

    EnrolmentFactory(child=child_with_user_guardian, occurrence=past_occurrence_1)

    executed = guardian_api_client.execute(CHILD_EVENTS_QUERY, variables=variables)
    # Still return enroled events if they are past events
    # Should only return past events from current project
    assert len(executed["data"]["child"]["pastEvents"]["edges"]) == 1
    snapshot.assert_match(executed)
