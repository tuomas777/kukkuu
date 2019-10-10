import factory
from django.contrib.auth.hashers import make_password
from factory.random import randgen

from children.models import Child, Relationship
from users.factories import UserFactory


class ChildFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthdate = factory.Faker("date_this_year", before_today=True, after_today=False)
    social_security_number_hash = factory.LazyFunction(
        lambda: make_password(randgen.random())
    )

    class Meta:
        model = Child


class RelationshipFactory(factory.django.DjangoModelFactory):
    child = factory.SubFactory(ChildFactory)
    user = factory.SubFactory(UserFactory)
    type = factory.Faker(
        "random_element", elements=[t[0] for t in Relationship.TYPE_CHOICES]
    )

    class Meta:
        model = Relationship
