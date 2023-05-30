from rest_framework import viewsets, mixins
from rest_framework import filters
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from recipes.models import Category, Recipe, Ingredient, RecipeImage
from recipes.serializers import CategorySerializer, RecipeSerializer, \
    CreateUpdateRecipeSerializer, IngredientSerializer, RecipeImageSerializer
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
    queryset = Recipe.objects.select_related('category').all()
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

    def get_queryset(self):
        recipe_pk = self.kwargs['recipe_pk']
        recipe = Recipe.objects.filter(pk=recipe_pk).first()
        if not recipe:
            raise NotFound(detail=f'Recipe with id {recipe_pk} was not found')
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(recipe_id=self.kwargs['recipe_pk'])


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
        return super().get_queryset()

    def perform_create(self, serializer):
        recipe_pk = self.kwargs['recipe_pk']
        number_of_images = RecipeImage.objects.filter(
            recipe__id=recipe_pk).count()
        print(number_of_images)
        max_number_of_images = 3
        if number_of_images == max_number_of_images:
            raise MethodNotAllowed(
                method='POST',
                detail=f'The recipe already has the maximum number of images {max_number_of_images}'
            )
        else:
            serializer.save(recipe_id=self.kwargs['recipe_pk'])
