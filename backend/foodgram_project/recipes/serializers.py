from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, RecipeIngredient
from users.serializers import UserSerializer
# from django.contrib.auth import get_user_model

# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     """Сериализатор модели Юзер."""

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name')


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


class RecipeIngredientSeriaizer(serializers.ModelSerializer):
    """Сериализатор модели РецептИнгредиент. В него добавлены 3 поля из модели
    Ингредиент, через внутреннее поле 'ForeignKey' этого сериализатора под
    названием Ингредиент. А также добавлено одно поле из родной модели
    РецептИнгредиент под названиме Амаунт."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт."""

    ingredients = RecipeIngredientSeriaizer(source='recipeingredient_set',
                                            many=True)
    tags = TagSerializer(many=True)
    author = UserSerializer()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')
