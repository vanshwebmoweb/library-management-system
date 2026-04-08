import django_filters
from library.models import Book


class BookFilter(django_filters.FilterSet):
    author_name = django_filters.CharFilter(field_name='author__name',lookup_expr='icontains',label='Author name contains')

    category_name = django_filters.CharFilter(field_name='category__name',lookup_expr='icontains',label='Category name contains')

    title = django_filters.CharFilter(field_name='title',lookup_expr='icontains',label='Title contains')

    is_available = django_filters.BooleanFilter(field_name='copies_available',method='filter_available',label='Is available')

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(copies_available__gt=0)
        return queryset.filter(copies_available=0)

    class Meta:
        model = Book
        fields = ('author_name', 'category_name', 'title', 'is_available',)