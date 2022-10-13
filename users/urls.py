from rest_framework import routers

from .views import AddressViewSet, UserViewSet

users_router = routers.SimpleRouter()

users_router.register('addresses', AddressViewSet)
users_router.register('users', UserViewSet)
urlpatterns = users_router.urls
