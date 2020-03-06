import django_filters
from django.utils import timezone
from graphql_relay import from_global_id

from events.models import Occurrence
from events.utils import convert_to_localtime_tz


class OccurrenceFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(lookup_expr="date", field_name="time")
    time = django_filters.TimeFilter(method="filter_by_time", field_name="time")
    upcoming = django_filters.BooleanFilter(
        method="filter_by_upcoming", field_name="time"
    )
    venue_id = django_filters.CharFilter(
        field_name="venue", method="filter_by_venue_global_id"
    )

    class Meta:
        model = Occurrence
        fields = ["date", "time", "upcoming", "venue_id"]

    def filter_by_time(self, qs, name, value):
        value = convert_to_localtime_tz(value)
        return qs.filter(**{name + "__time": value})

    def filter_by_upcoming(self, qs, name, value):
        if value:
            return qs.filter(**{name + "__gte": timezone.now()})
        return qs

    def filter_by_venue_global_id(self, qs, name, value):
        venue_id = from_global_id(value)[1]
        return qs.filter(venue_id=venue_id)
