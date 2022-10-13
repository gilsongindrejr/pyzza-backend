import uuid
from django.conf import settings
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
from stdimage import StdImageField
from rest_framework.authtoken.models import Token


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
    complement = models.CharField(_('complement'), max_length=100, blank=True)
    
    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
    
    def __str__(self):
        return self.zip_code
    

class CustomUserManager(UserManager):
    
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(max_length=50, unique=True)
    cpf = models.CharField(max_length=11)
    address = models.ForeignKey(Address, verbose_name=_("address"), on_delete=models.CASCADE, null=True, blank=True)
    image = StdImageField(_('image'), upload_to=get_file_path, variations={'thumb': (400, 400)}, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf']
    
    def __str__(self):
        return self.email
    
    objects = CustomUserManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
