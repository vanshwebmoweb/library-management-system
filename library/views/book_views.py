from rest_framework import viewsets
from library.models import Book
from library.serializers import BookSerializer
from library.permissions import IsAdminOrReadOnly
from library.filters import BookFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view



@extend_schema_view(
    list=extend_schema(
        summary='List all books',
        description='Returns a paginated list of all books. Supports filtering, searching and ordering.',
    ),
    create=extend_schema(
        summary='Create a book',
        description='Create a new book. Admin only.',
    ),
    retrieve=extend_schema(
        summary='Get a book',
        description='Returns details of a specific book.',
    ),
    update=extend_schema(
        summary='Update a book',
        description='Update a specific book. Admin only.',
    ),
    destroy=extend_schema(
        summary='Delete a book',
        description='Delete a specific book. Admin only.',
    ),
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter
    search_fields = ('title','author__name','category__name','isbn',)

    ordering_fields = ('title','copies_available',)

    ordering = ('title',)

    def get_queryset(self):
        return Book.objects.select_related('author', 'category').all()
