from django.db.models import Avg
from rest_framework import serializers
from rest_framework_nested.relations import NestedHyperlinkedIdentityField, NestedHyperlinkedRelatedField
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from recipes.models import Category, Recipe, Ingredient, RecipeImage, Review, Rating
from users.models import CustomUser


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    get_recipes = serializers.HyperlinkedIdentityField(
        view_name='category-get-recipes', read_only=True
    )

    class Meta:
        model = Category
        fields = [
            'url', 'id', 'title', 'slug', 'recipes_in_category', 'get_recipes'
        ]

    recipes_in_category = serializers.SerializerMethodField(
        method_name='count_recipes'
    )

    def count_recipes(self, category: Category):
        return Recipe.objects.filter(category__id=category.id).count()
########################################################################
########################################################################


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
########################################################################
########################################################################


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
########################################################################
########################################################################


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
########################################################################
########################################################################


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
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )

    class Meta:
        model = Review
        fields = [
            'url', 'id', 'content', 'author_name', 'author',
            'published', 'recipe_title', 'recipe'
        ]
########################################################################
########################################################################


class RatingSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='recipe-rating-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'recipe_pk': 'recipe__pk'
        }
    )

    recipe_title = serializers.ReadOnlyField(source='recipe.title')
    recipe = serializers.HyperlinkedRelatedField(
        view_name='recipe-detail', read_only=True
    )
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )

    class Meta:
        model = Rating
        fields = [
            'url', 'id', 'value', 'author_name',
            'author', 'published', 'recipe_title', 'recipe'
        ]
########################################################################
########################################################################


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )
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
            'url', 'id', 'title', 'slug', 'author_name', 'author',
            'category', 'instructions', 'published', 'list_ingredients',
            'ingredients', 'images', 'reviews_number', 'get_reviews', 'rating'
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

    rating = serializers.SerializerMethodField(
        method_name='count_ratings'
    )

    def count_ratings(self, recipe: Recipe):
        rating = Rating.objects.filter(recipe__id=recipe.id).aggregate(
            average_rating=Avg('value')
        )
        if rating['average_rating']:
            return rating['average_rating']
        else:
            return 'Recipe has not been rated by anyone yet'
########################################################################
########################################################################


class CreateUpdateRecipeSerializer(serializers.HyperlinkedModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    author = serializers.HyperlinkedRelatedField(
        view_name='author-detail', read_only=True
    )

    class Meta:
        model = Recipe
        fields = [
            'url', 'id', 'title', 'author_name', 'author',
            'category', 'instructions', 'published'
        ]
########################################################################
########################################################################


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='author-detail', read_only=True
    )

    get_recipes = serializers.HyperlinkedIdentityField(
        view_name='author-get-recipes', read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            'url', 'id', 'username', 'image', 'number_of_recipes', 'get_recipes'
        ]

    number_of_recipes = serializers.SerializerMethodField(
        method_name='count_recipes'
    )

    def count_recipes(self, customuser: CustomUser):
        return Recipe.objects.filter(author__id=customuser.id).count()
