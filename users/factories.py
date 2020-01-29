import factory
from django.contrib.auth import get_user_model

from users.models import Guardian


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()


class GuardianFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number")

    class Meta:
        model = Guardian

    @factory.post_generation
    def relationships(self, created, extracted, **kwargs):
        count = kwargs.pop("count", None)
        if count:
            from children.factories import RelationshipFactory

            RelationshipFactory.create_batch(count, guardian=self, **kwargs)
