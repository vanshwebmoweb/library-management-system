from rest_framework import serializers
from django.utils import timezone
from library.models import Book


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    category_name = serializers.CharField(source='category.name')
    is_available = serializers.CharField()
    availability_status = serializers.CharField()
    last_borrowed_user = serializers.CharField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_name', 'category', 'category_name', 'isbn', 'published_date', 'copies_available', 'is_available', 'availability_status', 'last_borrowed_user',)
        read_only_fields = ('id', 'author_name', 'category_name', 'is_available', 'availability_status', 'last_borrowed_user',)


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'isbn', 'published_date', 'copies_available',)

    def validate(self, data):
        title = data.get('title')
        isbn = data.get('isbn')
        copies_available = data.get('copies_available')
        published_date = data.get('published_date')

        if title:
            if len(title) < 2:
                raise serializers.ValidationError({"title_length": "Title must be at least 2 characters."})

        if isbn:
            if not isbn.isdigit():
                raise serializers.ValidationError({"isbn_contain_numbers": "ISBN must contain numbers only."})

        if copies_available is not None:
            if copies_available < 0:
                raise serializers.ValidationError({"copies_negative": "Copies available cannot be negative."})

        if published_date:
            if published_date > timezone.now().date():
                raise serializers.ValidationError({"published_date_infuture": "Published date cannot be in the future."})

        return data


class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'category', 'isbn', 'published_date', 'copies_available',)

    def validate(self, data):
        title = data.get('title')
        isbn = data.get('isbn')
        copies_available = data.get('copies_available')
        published_date = data.get('published_date')

        if title:
            if len(title) < 2:
                raise serializers.ValidationError({"title_length": "Title must be at least 2 characters."})

        if isbn:
            if not isbn.isdigit():
                raise serializers.ValidationError({"isbn_contain_numbers": "ISBN must contain numbers only."})

        if copies_available is not None:
            if copies_available < 0:
                raise serializers.ValidationError({"copies_negative": "Copies available cannot be negative."})

        if published_date:
            if published_date > timezone.now().date():
                raise serializers.ValidationError({"published_date_infuture": "Published date cannot be in the future."})

        return data


class BookRetrieveSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    category_name = serializers.CharField(source='category.name')
    is_available = serializers.CharField()
    availability_status = serializers.CharField()
    last_borrowed_user = serializers.CharField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_name', 'category', 'category_name', 'isbn', 'published_date', 'copies_available', 'is_available', 'availability_status', 'last_borrowed_user',)
        read_only_fields = ('id', 'author_name', 'category_name', 'is_available', 'availability_status', 'last_borrowed_user',)


class BookDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title',)
        read_only_fields = ('id', 'title',)