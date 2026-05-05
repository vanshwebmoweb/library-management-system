import django_filters
from library.models import Book

from django_filters.rest_framework import filterset
from django_filters import BaseInFilter, NumberFilter



class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title contains')
    is_available = django_filters.BooleanFilter(field_name='copies_available', method='filter_available', label='Is available')
    copies_exact = django_filters.NumberFilter(field_name='copies_available', label='Exact copies')
    copies_range = django_filters.RangeFilter(field_name='copies_available', label='Copies range',)
    copies_min = django_filters.NumberFilter(field_name='copies_available', lookup_expr='gte', label='Minimum copies',)
    copies_max = django_filters.NumberFilter(field_name='copies_available', lookup_expr='lte', label='Maximum copies',)
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte', label='Published after',)
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte', label='Published before',)
    author_id = NumberInFilter(field_name='author', lookup_expr='in', label='Filter by multiple Author IDs')
    sort_order = django_filters.ChoiceFilter(
        choices=[
            ('asc', 'Ascending'),
            ('desc', 'Descending'),
        ],
        method='filter_sort',
        label='Sort order',
    )

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(copies_available__gt=0)
        return queryset.filter(copies_available=0)

    def filter_sort(self, queryset, name, value):
        if value == 'asc':
            return queryset.order_by('title')
        return queryset.order_by('-title')

