from django.db import models
from django.contrib.auth import get_user_model
from colorfield.fields import ColorField

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)
    color = ColorField('Цвет в HEX', default='#FF0000')
    slug = models.SlugField('Уникальный слаг', unique=True, max_length=200)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=50)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение')
    text = models.TextField('Текст')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_tags(self):
        return ', '.join([p.name for p in self.tags.all()])

    def get_ingredients(self):
        return ', '.join([p.name for p in self.ingredients.all()])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='amount')
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.amount)