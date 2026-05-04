
from library.models import BorrowRecord
from library.serializers.borrow_serializer import (BorrowListSerializer, BorrowCreateSerializer, BorrowRetrieveSerializer, BorrowUpdateSerializer, BorrowDestroySerializer,)
from library.permissions import IsOwnerOrAdmin
from library.filters.borrow_filter import BorrowFilter

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics, permissions, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend


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
        if user.is_staff:
            filter_param = self.request.query_params.get('filter')
            if filter_param == 'borrowed':
                return BorrowRecord.objects.borrowed()
            elif filter_param == 'returned':
                return BorrowRecord.objects.returned()
            elif filter_param == 'active':
                return BorrowRecord.objects.active_borrows()
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.for_user(user)


class BorrowCreateView(generics.CreateAPIView):
    serializer_class = BorrowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BorrowRecord.objects.all()
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'borrow'

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        book.copies_available -= 1
        book.save()
        serializer.save(user=self.request.user)


class BorrowRetrieveView(generics.RetrieveAPIView):
    queryset = BorrowRecord.objects.select_related('user','book').all()
    serializer_class = BorrowRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class BorrowUpdateView(generics.UpdateAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()

        if old_status == 'borrowed' and instance.status == 'returned':
            instance.book.copies_available += 1
            instance.book.save()
            print(f"Copies increased to: {instance.book.copies_available}")


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


        serializer = BorrowCreateSerializer(data=data, many=True,)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)

        for item in serializer.validated_data:
            book = item['book']
            if book.copies_available < 1:
                return Response({"book_not_available": f"No copies available for {book.title}."}, status=status.HTTP_400_BAD_REQUEST,)


        borrow_records = [
            BorrowRecord(user=request.user, book=item['book'], status='borrowed',)
            for item in serializer.validated_data
        ]


        for item in serializer.validated_data:
            book = item['book']
            book.copies_available -= 1
            book.save()


        BorrowRecord.objects.bulk_create(borrow_records)

        return Response({"message": f"{len(borrow_records)} books borrowed successfully."}, status=status.HTTP_201_CREATED,)