from rest_framework import serializers
from .models import (Tag, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe,
                     ShoppingCart)

from users.serializers import ReUserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Тэг."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиент."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели РецептИнгредиент. В него добавлены 3 поля из модели
    Ингредиент, через внутреннее поле 'ForeignKey' этого сериализатора под
    названием Ингредиент. А также добавлено одно поле из родной модели
    РецептИнгредиент под названиме Амаунт."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт."""

    ingredients = RecipeIngredientSerializer(source='recipe_ingredient',
                                             many=True)
    tags = TagSerializer(many=True)
    author = ReUserSerializer()

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def validate(self, data):
        """
        Валидация создания рецепта.
        """
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Время приготовления указано не верно!.')
        if Recipe.objects.get(name=data['name']).exists() and (
                self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Такой рецепт уже существует')
        return data

    def get_is_favorited(self, obj):
        """
        Проверка добавлен ли рецепт в избранное.
        """
        user = self.context.get('request').user
        queryset = FavoriteRecipe.objects.filter(user=user.id,
                                                 recipe=obj.id).exists()
        return queryset

    def get_is_in_shopping_cart(self, obj):
        """
        Проверка добавлен ли рецепт в список покупок.
        """
        user = self.context.get('request').user
        queryset = ShoppingCart.objects.filter(user=user.id,
                                               recipe=obj.id).exists()
        return queryset


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Избранные.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')
        extra_kwargs = {'user': {'write_only': True},
                        'recipe': {'write_only': True}}

    def validate(self, data):
        """
        Валидация при добавлении рецепта в избранное.
        """
        if FavoriteRecipe.objects.filter(user=data['user'],
                                         recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже есть в избранном!')
        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Список Покупок.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ImageField(source='recipe.image', read_only=True)
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time', 'user', 'recipe')
        extra_kwargs = {'user': {'write_only': True},
                        'recipe': {'write_only': True}}

    def validate(self, data):
        """
        Валидация при добавлении рецепта в список покупок.
        """
        if ShoppingCart.objects.filter(user=data['user'],
                                       recipe=data['recipe']).exists():
            raise serializers.ValidationError('Рецепт уже есть в списке'
                                              ' покупок!')
        return data
