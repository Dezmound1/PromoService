from decimal import Decimal

from goods.models import Good


class GoodRepository:
    """Repository class for accessing good data."""

    @staticmethod
    def get_goods(goods_ids: list[int]) -> list[Good] | None:
        """Retrieves goods by their IDs."""
        return list(Good.objects.filter(id__in=goods_ids))

    @staticmethod
    def get_price(good_id: int) -> Decimal | None:
        """Retrieves the price of a single good by its ID."""
        good = Good.objects.filter(id=good_id).first()
        return good.price if good else None
