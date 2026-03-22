from rest_framework import serializers

from promo_service.goods.serializer import GoodSerializer

from .models import Order

from promo_service.promocode.serializers import DiscountPromoCodeSerializer


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating an order."""

    promo_code = DiscountPromoCodeSerializer()

    class Meta:
        model = Order
        fields = ["user_id", "total_amount", "promo_code"]


class OrderResponseSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""

    goods = GoodSerializer(many=True)  # TODO need to value fields of response
    promo_code = DiscountPromoCodeSerializer()  # TODO need to value fields of response

    class Meta:
        model = Order
        fields = ["id", "user", "goods", "promo_code", "total_price"]
        read_only_fields = fields
