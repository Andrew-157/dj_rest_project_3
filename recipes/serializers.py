from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from recipes.models import Category, Recipe, Ingredient


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug'
        ]


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    ingredients = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-ingredient-detail',
        parent_lookup_kwargs={'recipe_pk': 'recipe__pk'}
    )

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'slug', 'author', 'category', 'instructions', 'ingredients'
        ]


class CreateUpdateRecipeSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    ingredients = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-ingredient-detail',
        parent_lookup_kwargs={'recipe_pk': 'recipe__pk'}
    )

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'author', 'category', 'instructions', 'ingredients'
        ]


class IngredientSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='recipe-ingredient-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'recipe_pk': 'recipe__pk'
        }
    )

    recipe_title = serializers.ReadOnlyField(source='recipe.title')
    recipe = serializers.HyperlinkedRelatedField(
        view_name='recipe-detail', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = [
            'url', 'id', 'name', 'quantity',
            'units_of_measurement', 'recipe_title',
            'recipe'
        ]
