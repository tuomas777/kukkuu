import pytest
from django.contrib.auth import get_user_model

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
