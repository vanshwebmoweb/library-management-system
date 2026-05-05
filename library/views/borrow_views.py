
from library.models import BorrowRecord
from library.serializers.borrow_serializer import (BorrowListSerializer, BorrowCreateSerializer, BorrowRetrieveSerializer, BorrowUpdateSerializer, BorrowDestroySerializer,)
from library.permissions import IsOwnerOrAdmin
from library.filters.borrow_filter import BorrowFilter

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import F
from django.utils import timezone



class BorrowListView(generics.ListAPIView):
    serializer_class = BorrowListSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BorrowRecord.objects.none()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BorrowFilter
    search_fields = ('book__title', 'status',)
    ordering_fields = ('borrowed_date', 'return_date', 'status',)

    def get_queryset(self):
        user = self.request.user
        queryset = BorrowRecord.objects.select_related('user', 'book')

        if user.is_staff:
            filter_param = self.request.query_params.get('filter')
            if filter_param == 'borrowed':
                return queryset.borrowed()
            elif filter_param == 'returned':
                return queryset.returned()
            elif filter_param == 'active':
                return queryset.active_borrows()
            return queryset
        return queryset.for_user(user)



class BorrowCreateView(generics.CreateAPIView):
    serializer_class = BorrowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BorrowRecord.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'borrow'

    def perform_create(self, serializer):
        with transaction.atomic():
            book = serializer.validated_data['book']

            book.__class__.objects.filter(id=book.id).update(
            copies_available=F('copies_available') - 1
            )
            serializer.save(user=self.request.user)


class BorrowRetrieveView(generics.RetrieveAPIView):
    queryset = BorrowRecord.objects.select_related('user','book').all()
    serializer_class = BorrowRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class BorrowUpdateView(generics.UpdateAPIView):
    queryset = BorrowRecord.objects.select_related('book')
    serializer_class = BorrowUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        with transaction.atomic():
            instance = self.get_object()
            old_status = instance.status
            instance = serializer.save()

            if old_status == 'borrowed' and instance.status == 'returned':
                instance.book.__class__.objects.filter(id=instance.book.id).update(
                copies_available=F('copies_available') + 1
                )

                instance.return_date = timezone.now().date()
                instance.save()


class BorrowDestroyView(generics.DestroyAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowDestroySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class BorrowBulkCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        if not isinstance(data, list):
            return Response({"error": "Expected a list of borrow records."}, status=status.HTTP_400_BAD_REQUEST,)

        if len(data) == 0:
            return Response({"error": "List cannot be empty."}, status=status.HTTP_400_BAD_REQUEST,)

        with transaction.atomic():
            serializer = BorrowCreateSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)

            books = [item['book'] for item in serializer.validated_data]

            if len(books) != len(set(books)):
                raise serializers.ValidationError({"duplicate_books": "Duplicate books in request"})

            for book in books:
                if book.copies_available < 1:
                    raise serializers.ValidationError({"book_not_available": f"No copies available for {book.title}."})

            borrow_records = [
                BorrowRecord(user=request.user, book=book, status='borrowed')
                for book in books
            ]

            for book in books:
                book.__class__.objects.filter(id=book.id).update(
                copies_available=F('copies_available') - 1
                )

            BorrowRecord.objects.bulk_create(borrow_records)

        return Response({"message": f"{len(borrow_records)} books borrowed successfully."}, status=status.HTTP_201_CREATED,)