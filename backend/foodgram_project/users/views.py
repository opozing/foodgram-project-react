from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import (ReUserSerializer, UserCreateSerializer,
                          SubscriptionSerializer)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from djoser.serializers import UserSerializer
from rest_framework.views import APIView
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
        not_myself = request.user.id != author
        exist = Subscription.objects.filter(author=author,
                                            follower=request.user).exists()
        if not_myself:
            if request.method == 'GET' and not exist:
                # request = Subscription.objects.create(author=author,
                #                                       follower=request.user)
                # serializer = SubscriptionSerializer(request)
                # return Response(serializer.data)
                data = {'author': author, 'follower': follower}
                print(data)
                context = {'request': request}
                print(context)
                serializer = SubscriptionSerializer(data=data, context=context)
                if serializer.is_valid():
                    serializer.save(author=author, follower=follower)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif request.method == 'DELETE' and exist:
                request = Subscription.objects.get(author=author,
                                                   follower=request.user).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        
        

# class SubscriptionViewSet(viewsets.ModelViewSet):
#     queryset = Subscription.objects.all()
#     serializer_class = SubscriptionSerializer

    # def get_permissions(self):
    #     if self.action == "list":
    #         self.permission_classes = [permissions.AllowAny]

    # def list(self, request, *args, **kwargs):
    #     return Response(User.objects.all())
    
    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)

    # def detail(self, request, *args, **kwargs):
    #     return super(UserViewSet, self).detail(request, *args, **kwargs)

    # def get_permissions(self):
    #     # try:
    #           return [permission() for permission in self.permission_classes_by_action[self.action]]
    #     # except KeyError:
    #     #     return [permission() for permission in self.permission_classes]

# class APIUserList(APIView):
#     """Вью списка пользователей. При GET и POST запросах использует разные
#        сериализаторы."""

#     def get(self, request):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = UserCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class APIUserDetail(APIView):
#     # permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         users = get_object_or_404(User, pk=pk)
#         serializer = UserDetailSerializer(users)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         users = get_object_or_404(User, pk=pk)
#         serializer = UserDetailSerializer(users, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         users = get_object_or_404(User, pk=pk)
#         serializer = UserDetailSerializer(users, data=request.data,
#                                           partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         user = get_object_or_404(User, pk=pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class APIMeDetail(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         serializer = UserDetailSerializer(request.user)
#         if request.user.is_authenticated:
#             return Response(serializer.data)
#         # return Response(status=status.HTTP_403_FORBIDDEN)
