from rest_framework import serializers

from .models import Order

from promo_service.promocode.serializers import DiscountPromoCodeSerializer


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating an order."""

    promo_code = DiscountPromoCodeSerializer()

    class Meta:
        model = Order
        fields = ["user_id", "total_amount", "promo_code"]
