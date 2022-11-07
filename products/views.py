from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Category, Product

from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer     
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super(ProductsViewSet, self).get_queryset()

        filter = self.request.query_params.get('filter')
        search = self.request.query_params.get('search')

        if filter is not None:
            queryset = queryset.filter(category__name__iexact=filter)

        if search is not None:
            queryset = queryset.filter(name__icontains=search)

        return queryset