from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
# /categories/
# /categories/{pk}/

router.register(r'products', views.ProductViewSet, basename='product')
# /products/
# /products/{pk}/

categories_router = routers.NestedSimpleRouter(
    router, r'categories', lookup='category'
)
categories_router.register(
    r'products', views.ProductByCategoryViewSet, basename='category-product'
)
# /categories/{category_pk}/products/
# /categories/{category_pk}/products/{pk}/

products_router = routers.NestedSimpleRouter(
    router, r'products', lookup='product'
)

products_router.register(
    r'images', views.ProductImageViewSet, basename='product-image'
)
# /products/{product_pk}/images/
# /products/{product_pk}/images/{pk}/

products_images_router = routers.NestedSimpleRouter(
    categories_router, r'products', lookup='product')
products_images_router.register(
    r'images', views.ProductImageByCategoryViewSet, basename='category-product-image')

# /categories/{category_pk}/products/{product_pk}/images/
# /categories/{category_pk}/products/{product_pk}/images/{pk}/

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls)),
    path('', include(products_router.urls)),
    path('', include(products_images_router.urls))
]
