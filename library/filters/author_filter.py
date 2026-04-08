import django_filters
from library.models import Author


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains',label='Author name contains')

    class Meta:
        model = Author
        fields = ('name',)