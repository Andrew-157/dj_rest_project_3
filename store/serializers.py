from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from store.models import Category, Product, ProductImage


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = NestedHyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='category-product-detail',
        parent_lookup_kwargs={'category_pk': 'category__pk'}
    )

    class Meta:
        model = Category
        fields = ['url', 'id', 'title', 'products']


class ProductByCategorySerializer(NestedHyperlinkedModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='category-product-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'category_pk': 'category__pk'
        }
    )

    category_title = serializers.ReadOnlyField(source='category.title')
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail', read_only=True
    )

    images = NestedHyperlinkedRelatedField(
        view_name='product-image-detail',
        many=True,
        read_only=True,
        parent_lookup_kwargs={'product_pk': 'product__pk'}
    )

    class Meta:
        model = Product
        fields = ['url', 'title', 'description',
                  'number_in_stock', 'unit_price',
                  'category_title', 'category', 'images']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category_title = serializers.ReadOnlyField(source='category.title')
    category = serializers.HyperlinkedRelatedField(
        view_name='category-detail', read_only=True
    )
    images = NestedHyperlinkedRelatedField(
        view_name='product-image-detail',
        many=True,
        read_only=True,
        parent_lookup_kwargs={'product_pk': 'product__pk'}
    )

    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'description',
                  'number_in_stock', 'unit_price',
                  'category_title', 'category', 'images']


class ProductImageSerializer(serializers.ModelSerializer):
    url = NestedHyperlinkedIdentityField(
        view_name='product-image-detail',
        lookup_field='pk',
        parent_lookup_kwargs={
            'product_pk': 'product__pk'
        }
    )

    product_title = serializers.ReadOnlyField(source='product.title')
    product = serializers.HyperlinkedRelatedField(
        view_name='product-detail', read_only=True
    )

    class Meta:
        model = ProductImage
        fields = ['url', 'id', 'image', 'product_title', 'product']
