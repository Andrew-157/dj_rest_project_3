from django.db.models.query_utils import Q
from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from recipes.models import Category, Recipe, Ingredient, RecipeImage, Review
from recipes.serializers import CategorySerializer, RecipeSerializer, \
    CreateUpdateRecipeSerializer, IngredientSerializer, \
    CreateUpdateIngredientSerializer, RecipeImageSerializer, ReviewSerializer
from recipes.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly, IsParentObjectAuthorOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'slug']
    ordering_fields = ['title', 'slug']

    def destroy(self, request, *args, **kwargs):
        if Recipe.objects.filter(category_id=self.kwargs['pk']):
            raise MethodNotAllowed(method='DELETE',
                                   detail='There are recipes associated with this category, cannot delete it.')
        return super().destroy(request, *args, **kwargs)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.select_related('category').\
        select_related('author').all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'slug', 'category']
    ordering_fields = ['title', 'slug', 'category']

    def get_serializer_class(self):
        # We want user not to enter slug field
        # when posting a recipe as it is done automatically,
        # so RecipeSerializer that is called for safe methods contains slug
        # field and CreateUpdateSerializer does not
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        else:
            return CreateUpdateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.select_related('recipe').all()
    serializer_class = IngredientSerializer
    permission_classes = [
        IsParentObjectAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return IngredientSerializer
        else:
            return CreateUpdateIngredientSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        recipe = Recipe.objects.filter(pk=recipe_pk).first()
        if not recipe:
            raise NotFound(detail=f'Recipe with id {recipe_pk} was not found')
        return Ingredient.objects.select_related('recipe').\
            filter(recipe=recipe).all()

    def perform_create(self, serializer):
        # we check if the recipe already has an ingredient with
        # the name that the user enters
        # if it does, we do not allow method
        ingredient_name = str(self.request.data['name']).lower()
        ingredient = Ingredient.objects.filter(
            Q(name=ingredient_name) &
            Q(recipe__id=self.kwargs['recipe_pk'])
        ).first()
        if ingredient:
            raise MethodNotAllowed(method='POST',
                                   detail=f'Ingredient for this recipe with this name already exists')
        serializer.save(recipe_id=self.kwargs['recipe_pk'])

    def perform_update(self, serializer):
        # we check if the recipe has an ingredient with
        # the name that the user enters
        # if this ingredient is the one that is being updated
        # than we do nothing, if it is not, we do not allow method
        ingredient = Ingredient.objects.filter(pk=self.kwargs['pk']).first()
        ingredient_name = str(self.request.data['name']).lower()
        ingredient_with_name = Ingredient.objects.filter(
            Q(name=ingredient_name) &
            Q(recipe__id=self.kwargs['recipe_pk'])
        ).first()
        if ingredient_with_name and (ingredient_with_name != ingredient):
            raise MethodNotAllowed(method='PUT',
                                   detail=f'Ingredient for this recipe with this name already exists')
        return super().perform_update(serializer)


class RecipeImageViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = RecipeImage.objects.select_related('recipe').all()
    serializer_class = RecipeImageSerializer
    permission_classes = [
        IsParentObjectAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        recipe = Recipe.objects.filter(pk=recipe_pk).first()
        if not recipe:
            raise NotFound(detail=f'Recipe with id {recipe_pk} was not found')
        return RecipeImage.objects.\
            select_related('recipe').filter(recipe=recipe).all()

    def perform_create(self, serializer):
        recipe_pk = self.kwargs['recipe_pk']
        number_of_images = RecipeImage.objects.filter(
            recipe__id=recipe_pk).count()
        max_number_of_images = 3
        if number_of_images == max_number_of_images:
            raise MethodNotAllowed(
                method='POST',
                detail=f'The recipe already has the maximum number of images {max_number_of_images}'
            )
        else:
            serializer.save(recipe_id=self.kwargs['recipe_pk'])


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('recipe').\
        select_related('author').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        recipe = Recipe.objects.filter(pk=recipe_pk).first()
        if not recipe:
            raise NotFound(
                detail=f'Recipe with id {recipe_pk} was not found'
            )
        return Review.objects.select_related('recipe').\
            select_related('author').filter(recipe=recipe).all()

    def perform_create(self, serializer):
        recipe_pk = self.kwargs['recipe_pk']
        author_pk = self.request.user.id
        review = Review.objects.select_related('recipe').\
            select_related('author').filter(
                Q(recipe__id=recipe_pk) &
                Q(author__id=author_pk)
        ).first()
        if review:
            raise MethodNotAllowed(
                method='POST',
                detail='User cannot create more than one review per recipe'
            )
        else:
            serializer.save(
                recipe_id=recipe_pk,
                author_id=author_pk
            )
