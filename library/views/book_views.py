from library.models import Book, BorrowRecord
from library.serializers.book_serializer import BookSerializer
from library.permissions import IsAdminOrReadOnly
from library.filters.book_filter import BookFilter
from library.exports import generate_books_pdf, generate_books_excel

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Value, CharField
from django.db.models import Subquery, OuterRef
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.http import HttpResponse



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
    search_fields = ('title', 'author__name', 'category__name','isbn',)
    ordering_fields = ('title', 'copies_available',)

    def get_queryset(self):
        last_borrow_date = BorrowRecord.objects.filter(
            book=OuterRef('pk'),
        ).order_by('-borrowed_date').values('borrowed_date')[:1]

        return Book.objects.select_related('author', 'category').annotate(
            is_available=Case(
                When(copies_available__gt=0, then=Value('Yes')),
                default=Value('No'),
                output_field=CharField(),
            ),
            availability_status=Case(
            When(copies_available=0, then=Value('Out of Stock')),
            When(copies_available__lte=2, then=Value('Low Stock')),
            When(copies_available__lte=5, then=Value('Available')),
            When(copies_available__gt=5, then=Value('Well Stocked')),
            default=Value('Unknown'),
            output_field=CharField(),
        ),
            last_borrowed=Subquery(last_borrow_date),
            ).all()


    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        books_data = list(Book.objects.values('id','title','copies_available',))

        for book in books_data:
            book['is_available'] = 'Yes' if book['copies_available'] > 0 else 'No'

        return Response({'total_books': len(books_data),'books': books_data,})

    @action(
        detail=False,
        methods=['get'],
        url_path='export/pdf',
        permission_classes=[IsAdminOrReadOnly],
    )
    def export_pdf(self, request):
        books = Book.objects.select_related('author', 'category').all()

        buffer = generate_books_pdf(books)

        response = HttpResponse(buffer, content_type='application/pdf',)
        response['Content-Disposition'] = 'attachment; filename="books_report.pdf"'
        return response

    @action(
        detail=False,
        methods=['get'],
        url_path='export/excel',
        permission_classes=[IsAdminOrReadOnly],
    )
    def export_excel(self, request):
        books = Book.objects.select_related('author', 'category').all()

        buffer = generate_books_excel(books)

        response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)
        response['Content-Disposition'] = 'attachment; filename="books_report.xlsx"'
        return response


