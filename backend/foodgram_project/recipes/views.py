from .models import Tag, Ingredient, Recipe
from rest_framework import viewsets, permissions
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from rest_framework.filters import SearchFilter



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Ингредиент с поиском по началу поля Нейм"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
