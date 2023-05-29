from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from store.models import Category, Product, ProductImage, Brand


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['url', 'id', 'title', 'slug']


class BrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Brand
        fields = ['url', 'id', 'name', 'slug', 'logo']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    images = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='product-image-detail',
        parent_lookup_kwargs={'product_pk': 'product__pk'}
    )

    class Meta:
        model = Product
        fields = [
            'url', 'id', 'title', 'description',
            'number_in_stock', 'unit_price', 'last_update',
            'images', 'category',  'brand'
        ]


class CreateUpdateProductSerializer(serializers.HyperlinkedModelSerializer):
    category_title = serializers.ReadOnlyField(source='category.title')
    brand_title = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Product
        fields = [
            'url', 'id', 'title', 'description', 'number_in_stock',
            'unit_price', 'last_update',
            'category', 'brand', 'category_title', 'brand_title'
        ]


class ProductImageSerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='product-image-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'product_pk': 'product__pk'
        }
    )
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail', read_only=True
    )
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = ProductImage
        fields = ['url', 'id', 'image', 'product_title', 'product']
