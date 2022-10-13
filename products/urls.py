from rest_framework import routers

from .views import CategoryViewSet, ProductsViewSet

products_router = routers.SimpleRouter()

products_router.register('categories', CategoryViewSet)
products_router.register('products', ProductsViewSet)
urlpatterns = products_router.urls
