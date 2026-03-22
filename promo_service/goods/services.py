from promo_service.goods.repository import GoodRepository


class GoodService:
    """Service class for handling business logic related to goods."""

    def __init__(self, validated_data: dict):
        self.validated_data = validated_data
        self.good_repository = GoodRepository()

    def get_goods(self) -> list:
        """Retrieves goods based on the provided IDs."""
        goods_ids = self.validated_data.get("goods_id", [])
        return self.good_repository.get_goods(goods_ids)
