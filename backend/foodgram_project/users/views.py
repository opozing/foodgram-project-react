from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Subscription
from .serializers import ReUserSerializer, SubscriptionSerializer

User = get_user_model()


class ReUserViewSet(UserViewSet):
    """
    Общий вьюсет для всех эндпоинтов /users/.
    """
    queryset = User.objects.all()
    serializer_class = ReUserSerializer
    pagination_class = PageNumberPagination
    PageNumberPagination.page_size_query_param = 'limit'

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request):
        """
        Отображение страницы с подписками авторизованного пользователя.
        """
        user = self.request.user
        context = {'request': request}
        queryset = Subscription.objects.filter(follower=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionSerializer(page, context=context,
                                                many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionSerializer(queryset, context=context,
                                            many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        """
        Подписка и отписка от выбранного автора.
        """
        author = get_object_or_404(User, id=id).id
        follower = request.user.id
        exist = Subscription.objects.filter(author=author,
                                            follower=request.user).exists()

        if request.method == 'GET':
            data = {'author': author, 'follower': follower}
            context = {'request': request}
            serializer = SubscriptionSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE' and exist:
            Subscription.objects.get(author=author,
                                     follower=request.user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы не подписаны на автора'},
                        status=status.HTTP_400_BAD_REQUEST)
