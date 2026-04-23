from rest_framework import serializers
from django.utils import timezone
from library.models import Book



class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name')
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_name', 'category', 'category_name', 'isbn', 'published_date', 'days_since_published', 'copies_available', 'author_url', 'category_url', 'self_url',)
        read_only_fields = ('id', 'author_url', 'category_url', 'self_url', 'author_name', 'category_name',)


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
