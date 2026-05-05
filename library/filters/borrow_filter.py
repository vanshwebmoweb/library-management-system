import django_filters
from library.models import BorrowRecord


class BorrowFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[('borrowed', 'Borrowed'),('returned', 'Returned'),])