import django_filters
from library.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains',label='Title contains')
    is_available = django_filters.BooleanFilter(field_name='copies_available',method='filter_available',label='Is available')

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(copies_available__gt=0)
        return queryset.filter(copies_available=0)