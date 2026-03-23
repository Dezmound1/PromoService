from decimal import Decimal

from goods.models import Good
from promocode.models import DiscountPromoCode
from users.models import User

from .models import Order


class OrderRepository:
    """Repository class for accessing order data."""

    @staticmethod
    def create(
        user: User,
        goods: list[Good],
        total_price: Decimal,
        promo_code: DiscountPromoCode | None = None,
    ) -> Order:
        """
        Create a new order and attach goods to it.

        Parameters
        ----------
        user : User
            The user placing the order.
        goods : list[Good]
            The list of goods to include in the order.
        total_price : Decimal
            The total price of the order after discounts.
        promo_code : DiscountPromoCode | None
            The promo code applied, if any.

        Returns
        -------
        Order
            The created order instance.
        """
        order = Order.objects.create(
            user=user,
            total_price=total_price,
            promo_code=promo_code,
        )
        order.goods.set(goods)
        return order

    @staticmethod
    def count_promo_usages(promo_code_id: int) -> int:
        """
        Count the total number of times a promo code has been used.

        Parameters
        ----------
        promo_code_id : int
            The ID of the promo code.

        Returns
        -------
        int
            The number of orders using this promo code.
        """
        return Order.objects.filter(promo_code_id=promo_code_id).count()

    @staticmethod
    def has_user_used_promocode(user_id: int, promo_code_id: int) -> bool:
        """
        Check if a user has already used a specific promo code.

        Parameters
        ----------
        user_id : int
            The ID of the user.
        promo_code_id : int
            The ID of the promo code.

        Returns
        -------
        bool
            True if the user has already used this promo code, False otherwise.
        """
        return Order.objects.filter(
            user_id=user_id, promo_code_id=promo_code_id
        ).exists()
