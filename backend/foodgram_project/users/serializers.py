from rest_framework import serializers, validators, permissions
from djoser.serializers import UserCreateSerializer, UserSerializer
from .models import Subscription
from django.contrib.auth import get_user_model
from recipes.models import Recipe

User = get_user_model()


class ReUserSerializer(UserSerializer):
    """Сериализатор модели Юзер GET запрос."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class ReUserCreateSerializer(UserCreateSerializer):
    """Сериализатор модели Юзер POST запрос."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name',
                  'password')
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True},
                        'email': {'required': True}, }


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    # recipes = ShortRecipeSerializer(many=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author.id)
        serializer = RecipeInSubscriptionSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        queryset = Recipe.objects.filter(author=obj.author.id).count()
        return queryset

