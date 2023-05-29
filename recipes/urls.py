from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipes import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'recipes', views.RecipeViewSet, basename='recipe')


urlpatterns = [
    path('', include(router.urls))
]
