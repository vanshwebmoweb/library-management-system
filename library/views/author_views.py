from library.models import Author
from library.serializers.author_serializer import (AuthorListSerializer, AuthorCreateSerializer, AuthorRetrieveSerializer, AuthorUpdateSerializer, AuthorDestroySerializer, )
from library.permissions import IsAdminOrReadOnly
from library.filters.author_filter import AuthorFilter

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from django.db.models import Count,Sum,Avg
from django.db.models.functions import Concat
from django.db.models import Value,CharField

from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter



class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('name', 'bio',)
    ordering_fields = ('name', 'id',)

    def get_queryset(self):
        return Author.objects.prefetch_related('books'
        ).annotate(total_books=Count('books'),
        total_copies=Sum('books__copies_available'),
        name_with_count=Concat('name',Value(' ('),Count('books'),Value(' books)'),output_field=CharField(),),)


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorRetrieveSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Author.objects.prefetch_related('books'
            ).annotate(
            total_books=Count('books'),
            total_copies=Sum('books__copies_available'),
            name_with_count=Concat('name',Value(' ('),Count('books'),Value(' books)'),output_field=CharField(),),
            )


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorDestroyView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorDestroySerializer
    permission_classes = [IsAdminOrReadOnly]