from rest_framework import serializers
from recipes.models import Category, Recipe


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug'
        ]


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'author', 'category', 'instructions'
        ]
