from django.contrib import admin

from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class Product(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'category', 'description')