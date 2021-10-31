from .models import (Tag, Ingredient, Recipe, FavoriteRecipe, ShoppingCart,
                     RecipeIngredient)
from django.http import HttpResponse

from rest_framework import viewsets, permissions, status
from .permissions import IsOwnerOrReadOnly
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, FavoriteRecipeSerializer,
                          ShoppingCartSerializer)
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        """
        Метод создания - удаления обьекта подписки.
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
        return Response({'errors': 'Этого рецепта нет в избранном!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'DELETE'],
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        """
        Метод создания - удаления обьекта в списке покупок.
        """
        recipe = get_object_or_404(Recipe, id=pk).id
        user = self.request.user.id
        exist = ShoppingCart.objects.filter(user=user,
                                            recipe=recipe).exists()

        if request.method == 'GET':
            data = {'user': user, 'recipe': recipe}
            context = {'request': request}
            serializer = ShoppingCartSerializer(data=data,
                                                context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE' and exist:
            ShoppingCart.objects.get(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Этого рецепта нет в списке покупок!'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def download_shopping_cart(self, request):
        """
        Скачивание списка покупок.
        """
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user.id) # все обьекты моего списка покупок
        recipes = []  # создаем пустой список 
        for i in shopping_cart:
            recipes.append(i.recipe) # добавляем в новый список все обьекты (shopping_cart поле recipe)
        recipe_ingredients = []
        for i in recipes:
            recipe_ingredients += RecipeIngredient.objects.filter(recipe=i)
        ingredients_count = {}
        for i in recipe_ingredients: # обьекты модели recipe_ingredients
            if i.ingredient in ingredients_count:
                ingredients_count[i.ingredient] += i.amount
                break
            ingredients_count[i.ingredient] = i.amount  # в ключ даем ingredient, в значение - amount
        result = ''
        for ingredient in ingredients_count:
            print(ingredient, '11111111111111')
            weight = 0
            weight += ingredients_count[ingredient]
            result += (f'{ingredient.name} - {str(weight)} '
                       f'{ingredient.measurement_unit}.')
        download = open("buy_list.txt", "w+")
        download.write(result)
        download.close()
        read_file = open("buy_list.txt", "r")
        response = HttpResponse(read_file.read(),
                                content_type="text/plain,charset=utf8")
        read_file.close()
        response['Content-Disposition'] = (
            'attachment; filename="{}.txt"'.format('file_name'))
        return response
