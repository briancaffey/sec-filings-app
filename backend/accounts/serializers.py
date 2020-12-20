from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Subscription

User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = (
            'valid_through',
            'stripe_customer_id',
            'stripe_subscription_id',
        )


class UserSerializer(serializers.ModelSerializer):

    subscription = SubscriptionSerializer()

    class Meta:
        model = User
        fields = (
            'email',
            'is_staff',
            'is_active',
            'is_superuser',
            'is_premium',
            'subscription',
        )
