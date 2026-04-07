from rest_framework import generics, permissions
from library.models import BorrowRecord
from library.serializers import BorrowRecordSerializer
from library.permissions import IsOwnerOrAdmin
from library.filters import BorrowFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend



class BorrowListView(generics.ListAPIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BorrowRecord.objects.none()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BorrowFilter
    search_fields = ('book__title', 'status',)

    ordering_fields = ('borrowed_date','return_date','status',)

    ordering = ('-borrowed_date',)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return BorrowRecord.objects.all()
        return BorrowRecord.objects.filter(user=user)


class BorrowCreateView(generics.CreateAPIView):
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = BorrowRecord.objects.all()

    def perform_create(self, serializer):
        book = serializer.validated_data['book']
        book.copies_available -= 1
        book.save()
        serializer.save(user=self.request.user)


class BorrowRetrieveView(generics.RetrieveAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class BorrowUpdateView(generics.UpdateAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]


class BorrowDestroyView(generics.DestroyAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]