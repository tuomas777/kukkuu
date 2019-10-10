import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from ..factories import ChildFactory, RelationshipFactory
from ..models import Child

User = get_user_model()


@pytest.mark.django_db
def test_child_creation():
    ChildFactory()

    assert Child.objects.count() == 1


@pytest.mark.django_db
def test_relationship_creation():
    RelationshipFactory()

    assert Child.objects.count() == 1
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_social_security_number_setting():
    child = ChildFactory(social_security_number="777")

    assert check_password("777", child.social_security_number_hash)


@pytest.mark.django_db
def test_social_security_number_getting_is_prohibited():
    child = ChildFactory(social_security_number="777")

    with pytest.raises(AttributeError):
        c = child.social_security_number  # noqa
