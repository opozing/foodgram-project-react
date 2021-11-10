from django.contrib.auth.models import User
from django.test import Client, TestCase
from rest_framework import status
from rest_framework.test import APIClient

from recipes.models import FavoriteRecipe, Recipe, ShoppingCart


class RecipesViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username="sergey",)
        cls.recipe = Recipe.objects.create(name='test_recipe',
                                           cooking_time=1,
                                           author=cls.user)

        cls.url_favorite = ('/api/recipes/1/favorite/')
        cls.url_shopping_cart = ('/api/recipes/1/shopping_cart/')

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = APIClient()
        self.authorized_client.force_login(self.user)
        self.authorized_client.force_authenticate(self.user)

    def test_authorized_client_create_favorite(self):
        """
        Проверка добавления рецепта в избранное авторизованым юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.authorized_client.get(self.url_favorite)
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
        response = self.authorized_client.get(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.authorized_client.get(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_client_delete_favorite(self):
        """
        Проверка удаления рецепта из избранного авторизованым юзером.
        """
        response = self.authorized_client.get(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.authorized_client.delete(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorized_client_delete_favorite_double(self):
        """
        Проверка удаления рецепта котрого нет в избранном авторизованым юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.authorized_client.delete(self.url_favorite)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_client_create_favorite(self):
        """
        Проверка добавления рецепта в избранное Неавторизованым юзером.
        """
        response = self.guest_client.get(self.url_favorite)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(FavoriteRecipe.objects.count(), 0)

    def test_unauthorized_client_delete_favorite(self):
        """
        Проверка удаления рецепта из избранного Неавторизованым юзером.
        """
        response = self.authorized_client.get(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        response = self.guest_client.delete(self.url_favorite)
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_client_delete_favorite_double(self):
        """
        Проверка удаления рецепта которого нет в избранном Неавторизованым
        юзером.
        """
        self.assertEqual(FavoriteRecipe.objects.count(), 0)
        response = self.guest_client.delete(self.url_favorite)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_client_create_shopping_cart(self):
        """
        Проверка добавления рецепта в список покупок авторизованым юзером.
        """
        self.assertEqual(ShoppingCart.objects.count(), 0)
        response = self.authorized_client.get(self.url_shopping_cart)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(ShoppingCart.objects.get().recipe.name,
                         'test_recipe')

    def test_authorized_client_create_shopping_cart_double(self):
        """
        Проверка добавления рецепта который уже есть в списке покупок
        авторизованым юзером.
        """
        self.assertEqual(ShoppingCart.objects.count(), 0)
        response = self.authorized_client.get(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        response = self.authorized_client.get(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authorized_client_delete_shopping_cart(self):
        """
        Проверка удаления рецепта из списка покупок авторизованым юзером.
        """
        response = self.authorized_client.get(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        response = self.authorized_client.delete(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorized_client_delete_shopping_cart_double(self):
        """
        Проверка удаления рецепта котрого нет в списке покупок авторизованым
        юзером.
        """
        self.assertEqual(ShoppingCart.objects.count(), 0)
        response = self.authorized_client.delete(self.url_shopping_cart)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_guest_client_create_shopping_cart(self):
        """
        Проверка добавления рецепта в список покупок Неавторизованым юзером.
        """
        response = self.guest_client.get(self.url_shopping_cart)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(ShoppingCart.objects.count(), 0)

    def test_unauthorized_client_delete_shopping_cart(self):
        """
        Проверка удаления рецепта из списка покупок Неавторизованым юзером.
        """
        response = self.authorized_client.get(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        response = self.guest_client.delete(self.url_shopping_cart)
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_client_delete_shopping_cart_double(self):
        """
        Проверка удаления рецепта которого нет в списке покупок Неавторизованым
        юзером.
        """
        self.assertEqual(ShoppingCart.objects.count(), 0)
        response = self.guest_client.delete(self.url_shopping_cart)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
