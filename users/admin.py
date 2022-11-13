from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'state', 'city', 'neighborhood', 'street', 'house_number', 'complement')
    list_filter = ('state', 'city', 'neighborhood')
    search_fields = ('state', 'city', 'neighborhood', 'street', 'house_number', 'complement')


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'cpf', 'address')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'cpf')
    ordering = 'email',
    
    fieldsets = (
        (None, {"fields": ("image", "password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "cpf", "address")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("image", "first_name", "last_name", "cpf", "email", "password1", "password2", 'is_staff'),
            },
        ),
    )
