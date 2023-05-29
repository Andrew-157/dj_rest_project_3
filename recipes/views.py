from django.shortcuts import render
from rest_framework import viewsets
from recipes.models import Category
from recipes.serializers import CategorySerializer
from recipes.permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

