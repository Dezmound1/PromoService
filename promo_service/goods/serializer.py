from promo_service.goods.models import Good


class GoodSerializer:
    """Serializer for the Good model."""

    class Meta:
        model = Good
        fields = ["id", "name", "category", "price", "status"]
        read_only_fields = fields
