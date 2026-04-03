from rest_framework import viewsets
from library.models import Book
from library.serializers import BookSerializer
from library.permissions import IsAdminOrReadOnly



class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]