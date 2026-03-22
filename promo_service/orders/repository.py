from goods.models import Good
from users.models import User
from users.repository import UserRepository


class OrderRepository:
    """Repository class for accessing order data."""

    @staticmethod
    def create_order(validated_data: dict) -> None:
        """Creates a new order with the given user ID, total amount, and promo code."""

        current_user = OrderRepository.get_user(validated_data["user_id"])
        if not current_user:
            raise ValueError("User not found.")

    @staticmethod
    def get_user(user_id: int) -> User | None:
        """Retrieves a user by their ID."""
        return UserRepository.get_user(user_id)

    @staticmethod
    def get_goods(goods_id: list[int]) -> list[Good]:
        """Retrieves goods by their ID."""
        return list(Good.objects.filter(id__in=goods_id))
