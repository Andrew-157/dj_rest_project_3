from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from recipes.models import Category, Recipe, Ingredient, RecipeImage, Review


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug'
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
            'url', 'id', 'name', 'slug', 'quantity',
            'units_of_measurement', 'recipe_title',
            'recipe'
        ]


class CreateUpdateIngredientSerializer(NestedHyperlinkedModelSerializer):
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


class RecipeImageSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='recipe-image-detail',
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
        model = RecipeImage
        fields = [
            'url', 'id', 'image', 'recipe_title', 'recipe'
        ]


class ReviewSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='recipe-review-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'recipe_pk': 'recipe__pk'
        }
    )

    recipe_title = serializers.ReadOnlyField(source='recipe.title')
    recipe = serializers.HyperlinkedRelatedField(
        view_name='recipe-detail', read_only=True
    )
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Review
        fields = [
            'url', 'id', 'content', 'author', 'published', 'recipe_title', 'recipe'
        ]


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer()
    ingredients = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-ingredient-detail',
        parent_lookup_kwargs={'recipe_pk': 'recipe__pk'}
    )
    images = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-image-detail',
        parent_lookup_kwargs={
            'recipe_pk': 'recipe__pk'
        }
    )
    get_reviews = serializers.HyperlinkedIdentityField(
        view_name='recipe-get-reviews', read_only=True
    )

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'slug', 'author',
            'category', 'instructions', 'published', 'list_ingredients',
            'ingredients', 'images', 'reviews_number', 'get_reviews'
        ]

    list_ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )

    def get_ingredients(self, recipe: Recipe):
        ingredients = Ingredient.objects.filter(recipe__id=recipe.id).all()
        ingredients_list = []
        for ing in ingredients:
            if ing.units_of_measurement:
                ingredients_list.append(
                    f'{ing.quantity} {ing.units_of_measurement} of {ing.name.lower()}')
            else:
                ingredients_list.append(f'{ing.quantity} {ing.name.lower()}')
        return ingredients_list

    reviews_number = serializers.SerializerMethodField(
        method_name='count_reviews'
    )

    def count_reviews(self, recipe: Recipe):
        return Review.objects.filter(recipe__id=recipe.id).count()


class CreateUpdateRecipeSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'author', 'category', 'instructions', 'published'
        ]
