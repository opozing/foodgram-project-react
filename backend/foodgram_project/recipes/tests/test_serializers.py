from django.test import TestCase, Client
from django.contrib.auth.models import User
from recipes.models import (Recipe, FavoriteRecipe, ShoppingCart,
                            Tag)
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from recipes.serializers import (ShoppingCartSerializer,
                                 FavoriteRecipeSerializer)


class RecipesSerializerTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username="sergey",)
        cls.recipe = Recipe.objects.create(name='test_recipe',
                                           cooking_time=1,
                                           author=cls.user)

    def setUp(self):
        # self.guest_client = Client()
        # self.authorized_client = APIClient()
        # self.authorized_client.force_login(self.user)
        # self.authorized_client.force_authenticate(self.user)

        self.data = {
            'id': self.recipe.id,
            'name': self.recipe.name,
            'cooking_time': self.recipe.cooking_time,
            'user': self.user.id,
            'recipe': self.recipe.id
        }

    def test_favoriteserializer_create_object(self):
        """
        Проверка добавления рецепта в избранные.
        """
        serializer = FavoriteRecipeSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(FavoriteRecipe.objects.count(), 1)
        self.assertEqual(FavoriteRecipe.objects.get().recipe, self.recipe)

    def test_favoriteserializer_create_double(self):
        """
        Проверка невозможности добавления рецепта в избранные дважды.
        """
        serializer = FavoriteRecipeSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = FavoriteRecipeSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)

    def test_shopping_cart_serializer_create_object(self):
        """
        Проверка добавления рецепта в список покупок.
        """
        serializer = ShoppingCartSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(ShoppingCart.objects.count(), 1)
        self.assertEqual(ShoppingCart.objects.get().recipe, self.recipe)

    def test_shopping_cart_serializer_create_double(self):
        """
        Проверка невозможности добавления рецепта в список покупок дважды.
        """
        serializer = ShoppingCartSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = ShoppingCartSerializer(data=self.data)
        self.assertEqual(serializer.is_valid(), False)