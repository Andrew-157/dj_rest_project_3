from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.response import Response
from store.serializers import CategorySerializer, ProductByCategorySerializer, ProductSerializer, ProductImageSerializer
from store.permissions import IsAdminOrReadOnly
from store.models import Category, Product, ProductImage


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
            if self.request.method in SAFE_METHODS:
                raise NotFound(detail='No category was found with this id')
            # elif self.request.method == 'POST':
            #     raise MethodNotAllowed(
            #         detail='Method is not allowed for a nonexisting category')
        return Product.objects.\
            select_related('category').\
            filter(category=self.kwargs['category_pk'])

    def perform_create(self, serializer):
        category = Category.objects.filter(
            pk=self.kwargs['category_pk']).first()
        if not category:
            raise MethodNotAllowed(method='POST',
                                   detail='Method is not allowed for a nonexisting category')
        serializer.save(category_id=self.kwargs['category_pk'])


class ProductViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProductImageViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = ProductImage.objects.select_related('product').all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        product = Product.objects.filter(pk=self.kwargs['product_pk']).first()
        if not product:
            raise NotFound(detail='Product with this id was not found')
        return ProductImage.objects.\
            select_related('product').\
            filter(product__pk=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_pk'])
