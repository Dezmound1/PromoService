from decimal import Decimal

import structlog
from django.db import transaction
from rest_framework.exceptions import ValidationError

from goods.models import Good
from goods.repository import GoodRepository
from orders.repository import OrderRepository
from promocode.services import PromoCodeService
from users.models import User

logger = structlog.get_logger(__name__)


class OrderService:
    """Service for order operations."""

    @staticmethod
    def create_order(
        user: User, goods_data: list[dict], promo_code: str | None
    ) -> dict:
        """
        Create a new order with optional promo code.

        Parameters
        ----------
        user : User
            The user creating the order.
        goods_data : list[dict]
            List of dictionaries containing 'good_id' and 'quantity'.
        promo_code_str : str | None
            The promo code to apply, if any.

        Returns
        -------
        dict
            Response data matching OrderResponseSerializer format.
        """
        log = logger.bind(user_id=user.id, promo_code=promo_code)

        good_ids = [item["good_id"] for item in goods_data]
        goods = GoodRepository.get_goods(good_ids)

        if len(goods) != len(good_ids):
            log.warning("order.goods_not_found", requested=good_ids)
            raise ValidationError("Один или несколько товаров не найдены")

        goods_map = {good.id: good for good in goods}
        quantity_map = {item["good_id"]: item["quantity"] for item in goods_data}

        promo = PromoCodeService.validate(promo_code, user.id) if promo_code else None

        goods_response = []
        total_price = Decimal("0")
        total_discount = Decimal("0")

        for good_id, quantity in quantity_map.items():
            good: Good = goods_map[good_id]
            item_price = good.price * quantity

            if promo and PromoCodeService.is_discount_applicable(good, promo):
                item_discount = PromoCodeService.calculate_discount(item_price, promo)
            else:
                item_discount = Decimal("0")

            item_total = item_price - item_discount
            goods_response.append(
                {
                    "good_id": good_id,
                    "quantity": quantity,
                    "price": item_price,
                    "discount": str(item_discount),
                    "total": item_total,
                }
            )

            total_price += item_price
            total_discount += item_discount

        order_total = total_price - total_discount

        with transaction.atomic():
            order = OrderRepository.create(
                user=user,
                goods=goods,
                promo_code=promo,
                total_price=order_total,
            )

        log.info(
            "order.completed",
            order_id=order.id,
            total_price=str(total_price),
            total_discount=str(total_discount),
            order_total=str(order_total),
            goods_count=len(goods),
        )

        return {
            "user_id": user.id,
            "order_id": order.id,
            "goods": goods_response,
            "price": total_price,
            "discount": str(promo.discount_percent / Decimal("100")) if promo else "0",
            "total": order_total,
        }
