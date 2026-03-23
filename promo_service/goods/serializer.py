from rest_framework import serializers


class RequestGoodSerializer(serializers.Serializer):
    """Serializer for good items in the order request."""

    good_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class ResponseGoodSerializer(serializers.Serializer):
    """Serializer for good items in the order response."""

    good_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
