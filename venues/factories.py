import factory

from venues.models import Venue


class VenueFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=64)
    seat_count = factory.Faker("random_int", max=1000)

    class Meta:
        model = Venue
