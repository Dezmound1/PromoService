from rest_framework import serializers
from .models import DiscountPromoCode


class DiscountPromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for the DiscountPromoCode model."""

    class Meta:
        model = DiscountPromoCode
        fields = [
            "id",
            "code",
            "is_active",
            "valid_until",
            "usages",
            "discount_percent",
            "allowed_category",
        ]
        read_only_fields = fields
