from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    stripe_customer_id = models.CharField(max_length=1000, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
