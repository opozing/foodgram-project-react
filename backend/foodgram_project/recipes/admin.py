from django.contrib import admin

from .models import Tag, Ingredient, Recipe, RecipeIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = "-пусто-"


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    empty_value_display = "-пусто-"


class RecipeIngredientInline(admin.TabularInline):
    """Для отображения в админке поля ManyToMany ингредиентов c through"""

    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('id', 'get_tags', 'author', 'get_ingredients',
                    'name', 'image', 'text', 'cooking_time')
    empty_value_display = "-пусто-"


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    empty_value_display = "-пусто-"


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)