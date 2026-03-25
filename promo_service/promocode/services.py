from decimal import ROUND_HALF_UP, Decimal

import structlog
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from goods.models import Good
from orders.repository import OrderRepository
from promocode.models import DiscountPromoCode
from promocode.repository import PromoCodeRepository

logger = structlog.get_logger(__name__)


class PromoCodeService:
    """Service for validating and applying promo codes."""

    @staticmethod
    def validate(code: str, user_id: int) -> DiscountPromoCode:
        """
        Validate a promo code against business rules.

        Parameters
        ----------
        code : str
            The promo code string to validate.
        user_id : int
            The ID of the user attempting to use the promo code.

        Returns
        -------
        DiscountPromoCode
            The valid promo code instance.
        """
        log = logger.bind(promo_code=code, user_id=user_id)

        promo = PromoCodeRepository.get_by_code(code)

        if not promo:
            log.warning("promo.not_found")
            raise ValidationError("Промокод не найден")

        if not promo.is_active:
            log.warning("promo.inactive", promo_id=promo.id)
            raise ValidationError("Промокод неактивен")

        if promo.valid_until < timezone.now():
            log.warning(
                "promo.expired", promo_id=promo.id, valid_until=str(promo.valid_until)
            )
            raise ValidationError("Промокод просрочен")

        usage_count = OrderRepository.count_promo_usages(promo.id)
        if usage_count >= promo.max_usages:
            log.warning(
                "promo.usage_limit_reached",
                promo_id=promo.id,
                usage_count=usage_count,
                max_usages=promo.max_usages,
            )
            raise ValidationError("Лимит использований промокода исчерпан")

        if OrderRepository.has_user_used_promocode(user_id, promo.id):
            log.warning("promo.already_used_by_user", promo_id=promo.id)
            raise ValidationError("Вы уже использовали этот промокод")

        log.info(
            "promo.validated",
            promo_id=promo.id,
            discount_percent=str(promo.discount_percent),
        )
        return promo

    @staticmethod
    def is_discount_applicable(good: Good, promo: DiscountPromoCode) -> bool:
        """
        Check if a discount can be applied to a specific good.

        Parameters
        ----------
        good : Good
            The good instance to check.
        promo : DiscountPromoCode
            The promo code to apply.

        Returns
        -------
        bool
            True if the discount applies to this good.
        """
        if not good.promo_eligible:
            return False

        if promo.allowed_category and good.category != promo.allowed_category:
            return False

        return True

    @staticmethod
    def calculate_discount(price: Decimal, promo: DiscountPromoCode) -> Decimal:
        """
        Calculate the discount amount for a given price.

        Parameters
        ----------
        price : Decimal
            The original price.
        promo : DiscountPromoCode
            The promo code with discount percent.

        Returns
        -------
        Decimal
            The discount amount.
        """
        return (price * promo.discount_percent / Decimal("100")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
