from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe
from users.serializers import ReUserSerializer
# from drf_extra_fields.fields import Base64ImageField

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

    ingredients = RecipeIngredientSerializer(source='recipeingredient_set',
                                             many=True)
    tags = TagSerializer(many=True)
    author = ReUserSerializer()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        queryset = FavoriteRecipe.objects.filter(user=user.id,
                                                 recipe=obj.id).exists()
        return queryset


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Избранные.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    # image = Base64ImageField(source='recipe.image', read_only=True)
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
