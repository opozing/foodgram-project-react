from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import (ReUserSerializer, UserCreateSerializer, SubscriptionSerializer)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from djoser.serializers import UserSerializer
from rest_framework import status
from .models import Subscription
from rest_framework.decorators import action, permission_classes

User = get_user_model()


class ReUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = ReUserSerializer


    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        """
        Отображение страницы с подписками авторизованного пользователя.
        """
        user = self.request.user
        request = Subscription.objects.filter(follower=user)
        serializer = SubscriptionSerializer(request, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'DELETE'])
    def subscribe(self, request, id):
        """
        Метод подписки и отписки от выбранного автора.
        """
        author = get_object_or_404(User, id=id)
        follower = request.user
        exist = Subscription.objects.filter(author=author,
                                            follower=request.user).exists()

        if request.method == 'GET':
            data = {'author': author, 'follower': follower}
            context = {'request': request}
            serializer = SubscriptionSerializer(data=data, context=context)
            serializer.is_valid()
            serializer.save(author=author, follower=follower)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE' and exist:
            Subscription.objects.get(author=author,
                                     follower=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы не подписаны на автора'},
                        status=status.HTTP_400_BAD_REQUEST)
