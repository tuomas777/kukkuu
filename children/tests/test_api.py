import pytest
from graphene.utils.str_converters import to_snake_case

from users.models import Guardian

from ..models import Child, Relationship

SUBMIT_CHILD_MUTATION = """
mutation submitChild($input: SubmitChildMutationInput!) {
    submitChild(input: $input) {
        child {
            firstName
            lastName
            birthdate
        }
        relationship {
            type
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


CHILD_DATA = {"firstName": "Matti", "lastName": "Mainio", "birthdate": "2020-05-05"}


GUARDIAN_DATA = {
    "firstName": "Jussi",
    "lastName": "Juonio",
    "email": "jussi@example.com",
    "phoneNumber": "777-777777",
}


SUBMIT_CHILD_VARIABLES = {
    "input": {
        "child": CHILD_DATA,
        "guardian": GUARDIAN_DATA,
        "relationship": {"type": "PARENT"},
    }
}


def to_snake_dict(d):
    return {to_snake_case(k): v for k, v in d.items()}


@pytest.mark.django_db
def test_submit_child_unauthenticated(api_client):
    executed = api_client.execute(
        SUBMIT_CHILD_MUTATION, variables=SUBMIT_CHILD_VARIABLES
    )

    # TODO add better check when we have error codes
    assert "errors" in executed


@pytest.mark.django_db
def test_submit_child_authenticated(user_api_client):
    executed = user_api_client.execute(
        SUBMIT_CHILD_MUTATION, variables=SUBMIT_CHILD_VARIABLES
    )

    assert executed == {
        "data": {
            "submitChild": {
                "child": CHILD_DATA,
                "relationship": {"type": "PARENT"},
                "guardian": GUARDIAN_DATA,
            }
        }
    }

    # check that everything is created properly to the db
    child = Child.objects.get(**to_snake_dict(CHILD_DATA))
    guardian = Guardian.objects.get(**to_snake_dict(GUARDIAN_DATA))
    Relationship.objects.get(type=Relationship.PARENT, child=child, guardian=guardian)
