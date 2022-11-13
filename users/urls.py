from django.urls import path, include
from rest_framework import routers

from knox import views as knox_views
from .views import AddressViewSet, UserViewSet, RegisterAPI, LoginAPI, UserAPI, ChangePasswordAPI, UpdateUserAndAddressAPI

users_router = routers.SimpleRouter()

users_router.register('addresses', AddressViewSet)
users_router.register('users', UserViewSet)

urlpatterns = [
    path('auth/register', RegisterAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/user', UserAPI.as_view()),
    path('auth/change_password', ChangePasswordAPI.as_view()),
    path('auth/update_user', UpdateUserAndAddressAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view()),
]

urlpatterns += users_router.urls
