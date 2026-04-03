from rest_framework import serializers
from django.utils import timezone
from library.models import Book



class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'author_name', 'category', 'category_name', 'isbn', 'published_date', 'is_available',)

    def get_is_available(self, obj):
        if obj.copies_available > 0:
            return "Yes"
        return "No"

    def validate(self, data):
        title = data.get('title')
        isbn = data.get('isbn')
        copies_available = data.get('copies_available')
        published_date = data.get('published_date')

        if title:
            if len(title) < 2:
                raise serializers.ValidationError({"title": "Title must be at least 2 characters."})

        if isbn:
            if not isbn.isdigit():
                raise serializers.ValidationErro({"isbn": "ISBN must contain numbers only."})

        if copies_available is not None:
            if copies_available < 0:
                raise serializers.ValidationError({"copies_available": "Copies available cannot be negative."})

        if published_date:
            if published_date > timezone.now().date():
                raise serializers.ValidationError({"published_date": "Published date cannot be in the future."})

        return data