from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Author, Category, Book, BorrowRecord
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin1234',
            email='admin@gmail.com',
        )
        self.user = User.objects.create_user(
            username='john_doe',
            password='john1234',
            email='john@gmail.com',
        )
        self.author = Author.objects.create(
            name='Robert C. Martin',
            bio='American software engineer known for Clean Code',
        )

    def test_list_authors_no_auth(self):
        # anyone can list authors
        response = self.client.get('/api/authors')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author_as_admin(self):
        # admin can create author
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'J.K. Rowling',
            'bio': 'British author known for Harry Potter series',
        }
        response = self.client.post('/api/authors/create', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_as_regular_user(self):
        # regular user cannot create author
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'J.K. Rowling',
            'bio': 'British author known for Harry Potter series',
        }
        response = self.client.post('/api/authors/create', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_author_no_auth(self):
        # anonymous user cannot create author
        data = {
            'name': 'J.K. Rowling',
            'bio': 'British author known for Harry Potter series',
        }
        response = self.client.post('/api/authors/create', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin1234',
            email='admin@gmail.com',
        )
        self.user = User.objects.create_user(
            username='john_doe',
            password='john1234',
            email='john@gmail.com',
        )
        self.author = Author.objects.create(
            name='Robert C. Martin',
            bio='American software engineer known for Clean Code',
        )
        self.category = Category.objects.create(
            name='Programming',
        )
        self.book = Book.objects.create(
            title='Clean Code',
            author=self.author,
            category=self.category,
            isbn='1234567890',
            published_date='2008-08-01',
            copies_available=5,
        )

    def test_list_books_no_auth(self):
        response = self.client.get('/api/books')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_book(self):
        response = self.client.get(f'/api/books/{self.book.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'The Pragmatic Programmer',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '0987654321',
            'published_date': '1999-10-20',
            'copies_available': 3,
        }
        response = self.client.post('/api/books', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_as_regular_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'The Pragmatic Programmer',
            'author': self.author.id,
            'category': self.category.id,
            'isbn': '0987654321',
            'published_date': '1999-10-20',
            'copies_available': 3,
        }
        response = self.client.post('/api/books', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_books_by_title(self):
        response = self.client.get('/api/books?title=clean')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        response = self.client.get('/api/books?search=clean')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BorrowViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin1234',
            email='admin@gmail.com',
        )
        self.user = User.objects.create_user(
            username='john_doe',
            password='john1234',
            email='john@gmail.com',
        )
        self.author = Author.objects.create(
            name='Robert C. Martin',
            bio='American software engineer known for Clean Code',
        )
        self.category = Category.objects.create(
            name='Programming',
        )
        self.book = Book.objects.create(
            title='Clean Code',
            author=self.author,
            category=self.category,
            isbn='1234567890',
            published_date='2008-08-01',
            copies_available=5,
        )

    def test_list_borrows_no_auth(self):
        # anonymous cannot list borrows
        response = self.client.get('/api/borrows')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_borrows_authenticated(self):
        # logged in user can list borrows
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/borrows')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_borrow_book(self):
        self.client.force_authenticate(user=self.user)
        data = {'book': self.book.id}
        response = self.client.post('/api/borrows/create', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_borrow_book_reduces_copies(self):
        self.client.force_authenticate(user=self.user)
        data = {'book': self.book.id}
        self.client.post('/api/borrows/create', data)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 4)

    def test_borrow_unavailable_book(self):
        # set copies to 0
        self.book.copies_available = 0
        self.book.save()
        self.client.force_authenticate(user=self.user)
        data = {'book': self.book.id}
        response = self.client.post('/api/borrows/create', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_borrow_no_auth(self):
        data = {'book': self.book.id}
        response = self.client.post('/api/borrows/create', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)