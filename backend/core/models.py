from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class RequestLog(models.Model):
    """
    Request Log
    """

    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, blank=True
    )
    date = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=3000)
    full_path = models.CharField(max_length=3000)
    execution_time = models.IntegerField(null=True)
    response_code = models.PositiveIntegerField()
    method = models.CharField(max_length=10, null=True)
    remote_address = models.CharField(max_length=20, null=True)
