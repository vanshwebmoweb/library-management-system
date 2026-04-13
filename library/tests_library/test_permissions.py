from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from library.models import Author, Category, Book, BorrowRecord
from django.contrib.auth import get_user_model

User = get_user_model()


class PermissionTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin1234',
            email='admin@gmail.com',
        )
        self.user1 = User.objects.create_user(
            username='john_doe',
            password='john1234',
            email='john@gmail.com',
        )
        self.user2 = User.objects.create_user(
            username='sara_smith',
            password='sara1234',
            email='sara@gmail.com',
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
        self.borrow = BorrowRecord.objects.create(
            user=self.user1,
            book=self.book,
            status='borrowed',
        )

    def test_owner_can_update_borrow(self):
        # john can update his own borrow
        self.client.force_authenticate(user=self.user1)
        data = {
            'book': self.book.id,
            'status': 'returned',
            'return_date': '2026-04-09',
        }
        response = self.client.put(
            f'/api/borrows/{self.borrow.id}/update',
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_update_borrow(self):
        # sara cannot update john's borrow
        self.client.force_authenticate(user=self.user2)
        data = {
            'book': self.book.id,
            'status': 'returned',
            'return_date': '2026-04-09',
        }
        response = self.client.put(
            f'/api/borrows/{self.borrow.id}/update',
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_borrow(self):
        # admin can update anyone's borrow
        self.client.force_authenticate(user=self.admin)
        data = {
            'book': self.book.id,
            'status': 'returned',
            'return_date': '2026-04-09',
        }
        response = self.client.put(
            f'/api/borrows/{self.borrow.id}/update',
            data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_delete_any_book(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/books/{self.book.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_cannot_delete_book(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/books/{self.book.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)