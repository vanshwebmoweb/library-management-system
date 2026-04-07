from rest_framework import serializers
from django.utils import timezone
from library.models import BorrowRecord



class BorrowRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book_name = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = ('id', 'user', 'book', 'book_name', 'borrowed_date', 'return_date', 'status',)

    def validate(self, data):
        book = data.get('book')
        return_date = data.get('return_date')

        if book:
            if book.copies_available < 1:
                raise serializers.ValidationError({"book": "No copies available."})

        if return_date:
            if return_date < timezone.now().date():
                raise serializers.ValidationError({"return_date": "Return date cannot be in the past."})

        return data
