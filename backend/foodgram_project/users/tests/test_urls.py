from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username='sergey')
        cls.user2 = User.objects.create(username='sergey2')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_urls_unauthorized_user(self):
        """
        Доступность страниц неавторизованному юзеру
        """

        url_names = {
            '/api/users/': 200,
            '/api/users/1/': 401,
            '/api/users/subscriptions/': 401,
            '/api/users/1/subscribe/': 401,
            '/api/users/me/': 401,
        }

        for url, status in url_names.items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_urls_authorized_user(self):
        """
        Доступность страниц авторизованному юзеру
        """

        url_names = {
            '/api/users/': 200,
            '/api/users/1/': 200,
            '/api/users/subscriptions/': 200,
            '/api/users/2/subscribe/': 201,
            '/api/users/me/': 200,
        }

        for url, status in url_names.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)
