from rest_framework import viewsets
from library.models import Book
from library.serializers import BookSerializer
from library.permissions import IsAdminOrReadOnly
from library.filters import BookFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



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

