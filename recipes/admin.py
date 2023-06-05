from django.contrib import admin
from django.db.models import Avg
from django.utils.html import format_html
from recipes.models import Recipe, RecipeImage, Rating, Review, Category, Ingredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'slug', 'recipes'
    ]
    list_filter = [
        'title', 'slug'
    ]
    search_fields = [
        'title', 'slug'
    ]

    def recipes(self, obj):
        return Recipe.objects.\
            filter(category__id=obj.id).count()


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'instructions', 'slug',
        'category', 'author', 'published',
        'rating', 'reviews', 'ingredients'
    ]

    list_filter = [
        'category', 'published', 'author', 'title', 'slug'
    ]
    search_fields = [
        'title',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).\
            select_related('category', 'author')

    def rating(self, obj):
        rating = Rating.objects.filter(recipe__id=obj.id).\
            aggregate(average_rating=Avg('value'))
        if rating['average_rating']:
            return rating['average_rating']
        else:
            return 'Recipe has not been rated by anyone yet'

    def reviews(self, obj):
        return Review.objects.\
            filter(recipe__id=obj.id).count()

    def ingredients(self, obj):
        ingredients = Ingredient.objects.filter(recipe__id=obj.id).all()
        ingredients_list = []
        for ing in ingredients:
            if ing.units_of_measurement:
                ingredients_list.append(
                    f'{ing.quantity} {ing.units_of_measurement} of {ing.name.lower()}')
            else:
                ingredients_list.append(f'{ing.quantity} {ing.name.lower()}')
        return ingredients_list


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'recipe', 'author', 'content', 'published'
    ]
    list_filter = [
        'recipe', 'author', 'published'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).\
            select_related('author', 'recipe')


@admin.register(RecipeImage)
class RecipeImageAdmin(admin.ModelAdmin):
    list_display = [
        'recipe', 'image_tag'
    ]
    list_filter = [
        'recipe'
    ]
    readonly_fields = ['image']

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="50" height="50">')

    image_tag.short_description = 'Recipe image'
