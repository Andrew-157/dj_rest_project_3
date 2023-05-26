from rest_framework import viewsets, mixins
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.response import Response
from rest_framework import filters
from store.permissions import IsAdminOrReadOnly
from store.models import Category, Product, ProductImage, Brand
from store.serializers import CategorySerializer, ProductSerializer, \
    BrandSerializer, CreateUpdateProductSerializer, ProductImageSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        if Product.objects.select_related('category').filter(category_id=kwargs['pk']):
            raise MethodNotAllowed(method='DELETE',
                                   detail='There are products associated with this category')
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.\
        select_related('category').\
        select_related('brand').all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'brand__name', 'category__title']

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return ProductSerializer
        else:
            return CreateUpdateProductSerializer


class BrandViewSet(viewsets.ModelViewSet):
    # http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def destroy(self, request, *args, **kwargs):
        if Product.objects.select_related('brand').filter(brand_id=kwargs['pk']):
            raise MethodNotAllowed(method='DELETE',
                                   detail='There are products associated with this brand')
        return super().destroy(request, *args, **kwargs)


class ProductImageViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = ProductImage.objects.\
        select_related('product').all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        product = Product.objects.filter(pk=self.kwargs['product_pk']).first()
        if not product:
            raise NotFound(detail='No product with this id was found')
        return ProductImage.objects.select_related('product').\
            filter(product=self.kwargs['product_pk'])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_pk'])
