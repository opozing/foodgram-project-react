from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import Recipe
from rest_framework.test import APIClient


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_static_urls_unauthorized_user(self):
        url_names = {
            '/api/tags/': 200,
            '/api/ingredients/': 200,
        }

        for url, status in url_names.items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)


class RecipesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username="sergey",)
        cls.recipe = Recipe.objects.create(name='test_recipe',
                                           cooking_time=1,
                                           author=cls.user)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(self.user)

    def test_urls_unauthorized_user(self):
        """Доступность страниц  Неавторизованному юзеру"""

        url_names = {

            '/api/recipes/': 200,
            '/api/recipes/1/': 200,
            '/api/recipes/1/favorite/': 401,
            '/api/recipes/1/shopping_cart/': 401
        }

        for url, status in url_names.items():
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_urls_authorized_user(self):
        """Доступность страниц /recipes/ Aвторизованному юзеру"""

        url_names = {
            '/api/recipes/1/favorite/': 201,
            '/api/recipes/1/shopping_cart/': 201
        }

        for url, status in url_names.items():
            with self.subTest():
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, status)
