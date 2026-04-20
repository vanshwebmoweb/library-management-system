import django_filters
from library.models import Category


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',label='Category name contains',)