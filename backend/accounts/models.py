from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    username = None
    email = models.EmailField(_("email address"), unique=True)

    subscription = models.ForeignKey(
        "Subscription", null=True, on_delete=models.SET_NULL
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_premium(self):
        if self.subscription is not None:
            return self.subscription.valid_through > timezone.now()
        return False


class Subscription(models.Model):
    stripe_subscription_id = models.CharField(
        max_length=1000, blank=True, null=True
    )
    stripe_customer_id = models.CharField(
        max_length=1000, blank=True, null=True
    )
    valid_through = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        user = CustomUser.objects.filter(subscription=self).first()
        if user:
            return f"{str(user)} ({self.stripe_subscription_id})"
        else:
            return "No subscription"
