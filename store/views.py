from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from store.serializers import CategorySerializer, ProductByCategorySerializer
from store.permissions import IsAdminOrReadOnly
from store.models import Category, Product


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductByCategoryViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductByCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        category = Category.objects.filter(
            pk=self.kwargs['category_pk']).first()
        if not category:
            raise NotFound(detail='No category was found with this id')
        return Product.objects.\
            select_related('category').\
            filter(category=self.kwargs['category_pk'])

    def perform_create(self, serializer):
        serializer.save(category_id=self.kwargs['category_pk'])
