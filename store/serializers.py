from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from store.models import Category, Product, ProductImage


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        view_name='product-detail', read_only=True,
        many=True
    )

    class Meta:
        model = Category
        fields = ['url', 'id', 'title', 'products']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    category_title = serializers.ReadOnlyField(source='category.title')

    class Meta:
        model = Product
        fields = [
            'url', 'id', 'title', 'description',
            'number_in_stock', 'last_update',
            'category_title', 'category'
        ]
