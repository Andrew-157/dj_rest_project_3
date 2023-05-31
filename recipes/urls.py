from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from recipes import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')

recipes_router = routers.NestedSimpleRouter(
    router, r'recipes', lookup='recipe'
)
recipes_router.register(
    r'ingredients', views.IngredientViewSet, basename='recipe-ingredient'
)
recipes_router.register(
    r'images', views.RecipeImageViewSet, basename='recipe-image'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(recipes_router.urls))
]