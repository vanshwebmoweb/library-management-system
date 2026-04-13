from django.test import TestCase
from library.models import Author, Category, Book, BorrowRecord
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthorModelTest(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            name='Robert C. Martin',
            bio='American software engineer known for Clean Code',
        )

    def test_author_created_successfully(self):
        self.assertEqual(self.author.name, 'Robert C. Martin')
        self.assertEqual(self.author.bio, 'American software engineer known for Clean Code')

    def test_author_str(self):
        self.assertEqual(str(self.author), 'Robert C. Martin')

    def test_author_name_max_length(self):
        max_length = self.author._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='Programming',
        )

    def test_category_created_successfully(self):
        self.assertEqual(self.category.name, 'Programming')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Programming')

    def test_category_name_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Programming')


class BookModelTest(TestCase):

    def setUp(self):
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

    def test_book_created_successfully(self):
        self.assertEqual(self.book.title, 'Clean Code')
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.copies_available, 5)

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Clean Code')

    def test_book_isbn_unique(self):
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title='Another Book',
                author=self.author,
                category=self.category,
                isbn='1234567890',
                published_date='2020-01-01',
                copies_available=1,
            )


class BorrowRecordModelTest(TestCase):

    def setUp(self):
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
        self.borrow = BorrowRecord.objects.create(
            user=self.user,
            book=self.book,
            status='borrowed',
        )

    def test_borrow_created_successfully(self):
        self.assertEqual(self.borrow.user, self.user)
        self.assertEqual(self.borrow.book, self.book)
        self.assertEqual(self.borrow.status, 'borrowed')

    def test_borrow_str(self):
        self.assertEqual(
            str(self.borrow),
            f'{self.user} borrowed {self.book}'
        )

    def test_borrow_default_status(self):
        self.assertEqual(self.borrow.status, 'borrowed')