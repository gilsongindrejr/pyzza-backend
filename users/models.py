from django.db import models


class Address(models.Model):
    zip_code = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.CharField(max_length=10)
    complement = models.CharField(max_length=100)
