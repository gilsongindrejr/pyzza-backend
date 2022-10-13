from rest_framework import viewsets

from .models import Category, Product

from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer     
    queryset = Product.objects.all()
