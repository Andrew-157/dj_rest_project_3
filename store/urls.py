from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from store import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')

categories_router = routers.NestedSimpleRouter(
    router, r'categories', lookup='category'
)
categories_router.register(
    r'products', views.ProductByCategoryViewSet, basename='category-product'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(categories_router.urls))
]
