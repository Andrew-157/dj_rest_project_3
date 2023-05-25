from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from store.models import Category, Product, ProductImage, Brand


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['url', 'id', 'title']


class BrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Brand
        fields = ['url', 'id', 'name', 'logo']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = [
            'url', 'id', 'title', 'description',
            'number_in_stock', 'unit_price', 'last_update',
            'category',  'brand'
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
