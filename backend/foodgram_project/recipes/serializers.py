from rest_framework import serializers
from .models import (Tag, Ingredient, Recipe, RecipeIngredient, FavoriteRecipe,
                     ShoppingCart)
from django.shortcuts import get_object_or_404
from users.serializers import ReUserSerializer
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator

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


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт, GET запрос."""

    ingredients = RecipeIngredientSerializer(source='recipe_ingredient',
                                             many=True)
    tags = TagSerializer(many=True)
    author = ReUserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

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


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт, POST запрос."""

    author = ReUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(source='recipe_ingredient',
                                             many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    image = Base64ImageField()
    name = serializers.CharField(validators=[UniqueValidator(
        queryset=Recipe.objects.all(),
        message='Такой рецепт уже существует!')])

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')

    def validate(self, data):
        """
        Валидация создания рецепта.
        """
        if data['cooking_time'] < 1:
            raise serializers.ValidationError(
                'Время приготовления указано не верно!')
        # if Recipe.objects.filter(name=data['name']).exists() and (
        #         self.context['request'].method == 'POST'):
        #     raise serializers.ValidationError(
        #         'Такой рецепт уже существует!')
        return data

    def validate_tags(self, data):
        if not data:
            raise serializers.ValidationError(
                'Вы не добавили ни одного Тэга!')
        if len(data) != len(set(data)):
            raise serializers.ValidationError(
                'Тэг не может повторяться')
        return data

    def create_recipe_ingredient(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient.get('id'),
                recipe=recipe,
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        # print('validated_data------', validated_data)
        # print('initial_data-----', self.initial_data)
        # image = validated_data.pop('image')
        ingredients = self.initial_data.get('ingredients')
        validated_data.pop('recipe_ingredient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_recipe_ingredient(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        validated_data.pop('recipe_ingredient')
        ingredients = self.initial_data.get('ingredients')
        instance.name = validated_data['name']
        instance.text = validated_data['text']
        instance.cooking_time = validated_data['cooking_time']
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_recipe_ingredient(ingredients, instance)
        instance.save()
        return instance


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Избранные.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = Base64ImageField(source='recipe.image', read_only=True)
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
    image = Base64ImageField(source='recipe.image', read_only=True)
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
