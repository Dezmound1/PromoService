from rest_framework import serializers

from goods.serializer import RequestGoodSerializer, ResponseGoodSerializer


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating an order."""

    user_id = serializers.IntegerField()
    goods = RequestGoodSerializer(many=True, required=True, allow_empty=False)
    promo_code = serializers.CharField(
        required=False, allow_null=True, allow_blank=True, default=None
    )


class OrderResponseSerializer(serializers.Serializer):
    """Serializer for the order response."""

    user_id = serializers.IntegerField()
    order_id = serializers.IntegerField()
    goods = ResponseGoodSerializer(many=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
