import django_filters
from library.models import BorrowRecord


class BorrowFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[('borrowed', 'Borrowed'),('returned', 'Returned'),])

    book_name = django_filters.CharFilter(field_name='book__title',lookup_expr='icontains',label='Book name contains')

    class Meta:
        model = BorrowRecord
        fields = ('status', 'book_name',)