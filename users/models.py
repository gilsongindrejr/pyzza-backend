import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField


def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'users/{filename}'


class Address(models.Model):
    zip_code = models.CharField(_('zip code'),max_length=30)
    state = models.CharField(_('state'), max_length=30)
    city = models.CharField(_('city'), max_length=30)
    neighborhood = models.CharField(_('neighborhood'), max_length=30)
    street = models.CharField(_('street'), max_length=30)
    house_number = models.CharField(_('house number'), max_length=10)
    complement = models.CharField(_('complement'), max_length=100)
    

class User(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11)
    address = models.ForeignKey(Address, verbose_name=_("address"), on_delete=models.CASCADE)
    image = StdImageField(_('image'), upload_to=get_file_path, variations={'thumb': (400, 400)})

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'cpf']
    
    def __str__(self):
        return f'User: first_name: {self.first_name} last_name: {self.last_name} email: {self.email}'
