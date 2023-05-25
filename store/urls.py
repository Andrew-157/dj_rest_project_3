from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')

categories_router = routers.NestedSimpleRouter(
    router, r'categories', lookup='category'
)
categories_router.register(
    r'products', views.ProductByCategoryViewSet, basename='category-product'
)
products_router = routers.NestedSimpleRouter(
    router, r'products', lookup='product'
)

products_router.register(
    r'images', views.ProductImageViewSet, basename='product-image'
)
products_nested_router = routers.NestedSimpleRouter(
    categories_router, r'products', lookup='product')
products_nested_router.register(
    r'images', views.ProductImageByCategoryViewSet, basename='category-product-image')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
    path('', include(products_router.urls)),
    path('', include(products_nested_router.urls))
]
