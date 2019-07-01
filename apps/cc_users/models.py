from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CCUserManager


class BaseUser(AbstractUser):
    class Meta:
        abstract = True

    email = models.EmailField('Correu electrònic', blank=False, null=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
    objects = CCUserManager()

    @staticmethod
    def autocomplete_search_fields():
        filter_by = "id__iexact", "email__icontains", "first_name__icontains", "id_number__contains", \
                    "last_name__icontains", "surname2__icontains"
        return filter_by
