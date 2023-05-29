from rest_framework import serializers
from recipes.models import Category, Recipe, Ingredient


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug'
        ]
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'units_of_measurement']


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientSerializer(many=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'author', 'category', 'instructions', 'ingredients'
        ]

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        return recipe
