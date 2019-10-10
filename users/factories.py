import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.Faker("email")

    class Meta:
        model = get_user_model()

    @factory.post_generation
    def relationships(self, created, extracted, **kwargs):
        count = kwargs.pop("count", None)
        if count:
            from children.factories import RelationshipFactory

            RelationshipFactory.create_batch(count, user=self, **kwargs)
