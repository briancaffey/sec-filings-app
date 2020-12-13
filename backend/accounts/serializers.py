from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_staff',
            'is_superuser',
            'stripe_customer_id',
            'subscription_valid_through',
        )
