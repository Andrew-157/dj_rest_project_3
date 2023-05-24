from rest_framework import serializers
from rest_framework_nested.serializers import NestedHyperlinkedModelSerializer
from rest_framework_nested.relations import NestedHyperlinkedRelatedField, NestedHyperlinkedIdentityField
from store.models import Category, Product


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

    class Meta:
        model = Product
        fields = ['url', 'title', 'description',
                  'in_stock', 'unit_price', 'image',
                  'category_title', 'category']
