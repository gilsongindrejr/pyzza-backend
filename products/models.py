import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'products/{filename}'


class Category(models.Model):
    category = models.CharField(_('category'), max_length=30, null=False, blank=False)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        
    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(_('name'), max_length=50, null=False, blank=False)
    code = models.CharField(_('code'), max_length=100, null=False, blank=False)
    category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE, null=False, blank=False)
    price = models.DecimalField(_('price'), max_digits=5, decimal_places=2, null=False, blank=False)
    description = models.CharField(_('description'), max_length=200, blank=True)
    image = StdImageField(_('image'), upload_to=get_file_path, variations={'thumb': (400, 400)}, blank=True)
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
    
    def __str__(self):
        return self.name
    