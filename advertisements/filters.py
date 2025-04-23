from django_filters import rest_framework as filters
from advertisements.models import Advertisement, AdvertisementStatusChoices
from django.utils import timezone
from datetime import datetime, timezone as dt_timezone


class AdvertisementFilter(filters.FilterSet):
  """Фильтрация объявлений по дате, автору и статусу"""
  created_at_before = filters.CharFilter(method='filter_created_at_before')
  creator = filters.NumberFilter(field_name='creator__id', lookup_expr='exact')
  status = filters.ChoiceFilter(field_name='status', choices=AdvertisementStatusChoices.choices)

  class Meta:
    model = Advertisement
    fields = ['created_at_before', 'creator', 'status']

  def filter_created_at_before(self, queryset, name, value):
    """Метод переводит дату в запросе в формате 2025-04-14 в формат 2025-04-14T00:00:00Z"""
    try:
      naive_datetime = datetime.strptime(value, '%Y-%m-%d')
      aware_datetime = timezone.make_aware(naive_datetime, dt_timezone.utc)
      return queryset.filter(created_at__lte=aware_datetime)
    except ValueError:
      return queryset