from promo_service.goods.models import Good


class GoodRepository:
    """Repository class for accessing good data."""

    @staticmethod
    def get_goods(goods_ids: list[int]) -> list[Good] | None:
        """Retrieves goods by their IDs."""
        return list(Good.objects.filter(id__in=goods_ids))
