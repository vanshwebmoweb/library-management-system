from library.models import Author
from library.serializers.author_serializer import AuthorSerializer
from library.permissions import IsAdminOrReadOnly
from library.filters.author_filter import AuthorFilter

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from django.db.models import Count,Sum,Avg

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
        return Author.objects.annotate(total_books=Count('books'),
        total_copies=Sum('books__copies_available'),)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = list(serializer.data)
            for i, author in enumerate(page):
                data[i]['books'] = list(author.books.values_list('title', flat=True))
                data[i]['total_copies'] = author.total_copies
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = list(serializer.data)
        for i, author in enumerate(queryset):
            data[i]['books'] = list(author.books.values_list('title', flat=True))
            data[i]['total_copies'] = author.total_copies
        return Response(data)


class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorRetrieveView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Author.objects.annotate(
            total_books=Count('books'),
            total_copies=Sum('books__copies_available'),
            )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        data['books'] = list(
            instance.books.values_list('title', flat=True)
        )
        data['total_copies'] = instance.total_copies
        return Response(data)


class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]


class AuthorDestroyView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]