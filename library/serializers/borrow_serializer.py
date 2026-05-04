from rest_framework import serializers
from django.utils import timezone
from library.models import BorrowRecord


class BorrowListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username',)
    book_name = serializers.CharField(source='book.title',)

    class Meta:
        model = BorrowRecord
        fields = ('id', 'user', 'book', 'borrowed_date', 'return_date','status', 'user_name', 'book_name',)
        read_only_fields = ('id', 'user', 'borrowed_date', 'user_name', 'book_name',)


class BorrowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('book',)

    def validate(self, data):
        book = data.get('book')
        if book:
            if book.copies_available < 1:
                raise serializers.ValidationError({"book_not_available": "No copies available."})
        return data


class BorrowUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('book', 'status', 'return_date',)

    def validate(self, data):
        return_date = data.get('return_date')
        if return_date:
            if return_date < timezone.now().date():
                raise serializers.ValidationError({"return_date_inpast": "Return date cannot be in the past."})
        return data


class BorrowRetrieveSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username',)
    book_name = serializers.CharField(source='book.title',)

    class Meta:
        model = BorrowRecord
        fields = ('id', 'user', 'book', 'borrowed_date', 'return_date', 'status', 'user_name', 'book_name',)
        read_only_fields = ('id', 'user', 'borrowed_date', 'user_name', 'book_name',)


class BorrowDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowRecord
        fields = ('id', 'book', 'status',)
        read_only_fields = ('id', 'book', 'status',)