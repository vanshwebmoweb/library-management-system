from django.test import TestCase
from library.models import Author, Category, Book, BorrowRecord
from library.serializers import (
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    BorrowRecordSerializer,
)


class AuthorSerializerTest(TestCase):

    def test_valid_author_data(self):
        data = {
            'name': 'Robert C. Martin',
            'bio': 'American software engineer known for Clean Code',
        }
        serializer = AuthorSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_author_name_with_numbers(self):
        data = {
            'name': 'Robert123',
            'bio': 'American software engineer',
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_author_name_too_short(self):
        data = {
            'name': '',
            'bio': 'American software engineer',
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_author_bio_too_short(self):
        data = {
            'name': 'Robert',
            'bio': 'Short',
        }
        serializer = AuthorSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class CategorySerializerTest(TestCase):

    def test_valid_category_data(self):
        data = {'name': 'Programming'}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_category_name_numbers_only(self):
        data = {'name': '123'}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_category_name_too_short(self):
        data = {'name': 'AB'}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())


class BookSerializerTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            name='Robert C. Martin',
            bio='American software engineer known for Clean Code',
        )
        self.category = Category.objects.create(
            name='Programming',
        )

    def test_valid_book_data(self):
        data = {
            'title': 'Clean Code',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '1234567890',
            'published_date': '2008-08-01',
            'copies_available': 5,
        }
        serializer = BookSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_isbn_with_letters(self):
        data = {
            'title': 'Clean Code',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': 'ABC1234567',
            'published_date': '2008-08-01',
            'copies_available': 5,
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_negative_copies(self):
        data = {
            'title': 'Clean Code',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '1234567890',
            'published_date': '2008-08-01',
            'copies_available': -1,
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_future_published_date(self):
        data = {
            'title': 'Clean Code',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '1234567890',
            'published_date': '2099-08-01',
            'copies_available': 5,
        }
        serializer = BookSerializer(data=data)
        self.assertFalse(serializer.is_valid())