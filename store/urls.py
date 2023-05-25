from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet, basename='brand')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls))
]
