from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class ReUserSerializer(UserSerializer):
    """Сериализатор модели Юзер GET запрос."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        """
        Статус подписки пользователя на юзеров.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        queryset = Subscription.objects.filter(
            author=obj.id,
            follower=request.user.id).exists()
        return queryset


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
    """
    Внутреннее Поле Рецепты на странице с подписками пользователя.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Подписок.
    """
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')

    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count', 'author',
                  'follower')
        extra_kwargs = {'author': {'write_only': True},
                        'follower': {'write_only': True}}

    def get_is_subscribed(self, obj):
        """
        Статус подписки пользователя на юзеров.
        """
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        queryset = Subscription.objects.filter(
            author=obj.id,
            follower=request.user.id).exists()
        return queryset

    def get_recipes(self, obj):
        """
        Внутреннее поле Рецепты на странице подписок пользователя.
        """
        queryset = Recipe.objects.filter(author=obj.author.id)
        serializer = RecipeInSubscriptionSerializer(queryset, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """
        Количество рецептов у автора на которого подписан пользователь.
        """
        queryset = Recipe.objects.filter(author=obj.author.id).count()
        return queryset

    def validate(self, data):
        """
        Валидация при создании подписки на юзера.
        """
        if data['author'] == data['follower']:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        if Subscription.objects.filter(author=data['author'],
                                       follower=data['follower']).exists():
            raise serializers.ValidationError('Вы уже подписаны!')
        return data
