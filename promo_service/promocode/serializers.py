from rest_framework import serializers


class DiscountPromoCodeSerializer(serializers.ModelSerializer):
    """Serializer for the DiscountPromoCode model."""

    name = serializers.CharField(source="code")


# why using ModelSerializer?
