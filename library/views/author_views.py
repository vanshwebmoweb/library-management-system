from library.models import Author
from library.serializers import AuthorSerializer
from library.permissions import IsAdminOrReadOnly
from library.filters import AuthorFilter

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from django.db.models import Count

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter



class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuthorFilter
    search_fields = ('name', 'bio',)
    ordering_fields = ('name', 'id',)

    def get_queryset(self):
        return Author.objects.annotate(total_books=Count('books'))


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Author.objects.annotate(total_books=Count('books'))


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorDestroyView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]