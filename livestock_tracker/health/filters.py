import django_filters
from .models import HealthEvent


class HealthEventFilter(django_filters.FilterSet):
    animal_id = django_filters.NumberFilter()
    event_type = django_filters.ChoiceFilter(choices=HealthEvent.EVENT_TYPES)
    severity = django_filters.ChoiceFilter(choices=HealthEvent.SEVERITY_CHOICES)
    event_date_from = django_filters.DateTimeFilter(field_name='event_date', lookup_expr='gte')
    event_date_to = django_filters.DateTimeFilter(field_name='event_date', lookup_expr='lte')
    veterinarian = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = HealthEvent
        fields = ['animal_id', 'event_type', 'severity', 'event_date_from', 'event_date_to', 'veterinarian']