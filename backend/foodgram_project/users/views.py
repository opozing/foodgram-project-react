from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import (UserSerializer, UserCreateSerializer,
                          UserDetailSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя. При GET и POST запросах использует соответствующие
       разные сериализаторы."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method == 'GET':
                return UserSerializer
            if self.request.method == 'POST':
                return UserCreateSerializer


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
