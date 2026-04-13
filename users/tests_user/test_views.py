from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='john_doe',
            password='john1234',
            email='john@gmail.com',
            phone='9876543210',
            name='John Doe',
        )

    def test_register_user(self):
        data = {
            'username': 'new_user',
            'name': 'New User',
            'email': 'newuser@gmail.com',
            'phone': '9999999999',
            'password': 'newuser123',
        }
        response = self.client.post('/api/auth/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_duplicate_email(self):
        data = {
            'username': 'another_user',
            'name': 'Another User',
            'email': 'john@gmail.com',  # ← duplicate email
            'phone': '9999999999',
            'password': 'another123',
        }
        response = self.client.post('/api/auth/register', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        data = {
            'username': 'john_doe',
            'password': 'john1234',
        }
        response = self.client.post('/api/auth/login', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        data = {
            'username': 'john_doe',
            'password': 'wrongpassword',
        }
        response = self.client.post('/api/auth/login', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/auth/me')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'john_doe')

    def test_get_profile_not_authenticated(self):
        response = self.client.get('/api/auth/me')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)