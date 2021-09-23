from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели Юзер GET запрос."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор модели Юзер POST запрос."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор модели Юзер id GET запрос."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')
