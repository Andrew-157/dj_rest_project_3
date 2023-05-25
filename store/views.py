from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.response import Response
from store.permissions import IsAdminOrReadOnly
from store.models import Category, Product, ProductImage
from store.serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.\
        select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
