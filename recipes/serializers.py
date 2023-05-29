from rest_framework import serializers
from recipes.models import Category, Ingredient


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug'
        ]
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
