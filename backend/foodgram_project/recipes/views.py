from .models import Tag, Ingredient, Recipe, FavoriteRecipe
from rest_framework import viewsets, permissions, status
from .permissions import IsOwnerOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, FavoriteRecipeSerializer)
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response



class TagViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Тэг.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Ингредиент с поиском по началу поля Нейм.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Рецепт.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        """
        Вьюха создания - удаления обьекта подписки.
        """
        recipe = get_object_or_404(Recipe, id=pk).id
        user = self.request.user.id
        exist = FavoriteRecipe.objects.filter(user=user,
                                              recipe=recipe).exists()

        if request.method == 'GET':
            data = {'user': user, 'recipe': recipe}
            context = {'request': request}
            serializer = FavoriteRecipeSerializer(data=data,
                                                  context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and exist:
            FavoriteRecipe.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Этого рецепта нет в избранном!'})
