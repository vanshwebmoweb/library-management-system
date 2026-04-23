from rest_framework import serializers
from django.utils import timezone
from library.models import BorrowRecord



class BorrowRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('id', 'user', 'book', 'borrowed_date', 'return_date', 'status',)
        read_only_fields = ('id', 'user', 'borrowed_date',)

    def validate(self, data):
        book = data.get('book')
        return_date = data.get('return_date')

        if book:
            if book.copies_available < 1:
                raise serializers.ValidationError({"book_not_available": "No copies available."})

        if return_date:
            if return_date < timezone.now().date():
                raise serializers.ValidationError({"return_date_inpast": "Return date cannot be in the past."})

        return data
