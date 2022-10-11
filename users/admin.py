from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User

@admin.register('User')
class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'cpf', 'address')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'cpf')
    ordering = 'email',
    
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "cpf", "email")}),
        (_("Permissions"), { "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",),},),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("first_name", "last_name", "cpf", "email", "password1", "password2"),},),
    )
