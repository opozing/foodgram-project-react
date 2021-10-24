from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, FavoriteRecipe
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.serializers import IngredientSerializer, FavoriteRecipeSerializer


class RecipesViewsTests(TestCase):
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
        self.authorized_client.force_login(self.user)
        self.authorized_client.force_authenticate(self.user)

        self.url = ('/api/recipes/1/favorite/')
        self.favorite_data = {
            'id': self.recipe.id,
            'name': self.recipe.name,
            'cooking_time': self.recipe.cooking_time,
            'user': self.user.id,
            'recipe': self.recipe.id
        }

    def test_authorized_client_create_favorite(self):
        """
        Проверка добавления рецепта в избранное авторизованым юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.authorized_client.get(self.url, self.favorite_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(FavoriteRecipe.objects.get().recipe.name,
                         'test_recipe')

    def test_authorized_client_create_favorite_double(self):
        """
        Проверка добавления рецепта который уже есть в избранном
        авторизованым юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.authorized_client.get(self.url, self.favorite_data)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.authorized_client.get(self.url, self.favorite_data)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_client_delete_favorite(self):
        """
        Проверка удаления рецепта из избранного авторизованым юзером.
        """
        response = self.authorized_client.get(self.url, self.favorite_data)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.authorized_client.delete(self.url)
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorized_client_delete_favorite_double(self):
        """
        Проверка удаления рецепта котрого нет в избранном авторизованым юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.authorized_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_client_create_favorite(self):
        """
        Проверка добавления рецепта в избранное Неавторизованым юзером.
        """
        response = self.guest_client.get(self.url, self.favorite_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(FavoriteRecipe.objects.count(), 0)

    def test_unauthorized_client_delete_favorite(self):
        """
        Проверка удаления рецепта из избранного Неавторизованым юзером.
        """
        response = self.authorized_client.get(self.url, self.favorite_data)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.guest_client.delete(self.url)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_client_delete_favorite_double(self):
        """
        Проверка удаления рецепта которого нет в избранном Неавторизованым
        юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.guest_client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
