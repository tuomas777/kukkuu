import pytest
from django.contrib.auth import get_user_model

from children.models import Child

from ..factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_user_creation():
    UserFactory()
    assert User.objects.count() == 1
    assert Child.objects.count() == 0


@pytest.mark.django_db
def test_user_with_children_creation():
    UserFactory(relationships__count=3)
    assert User.objects.count() == 1
    assert Child.objects.count() == 3
    assert list(User.objects.first().children.all()) == list(Child.objects.all())
