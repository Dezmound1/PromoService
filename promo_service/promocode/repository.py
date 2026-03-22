from .models import DiscountPromoCode


class PromoCodeRepository:
    """Repository class for accessing promo code data."""

    @staticmethod
    def get_promo_code(code: str) -> DiscountPromoCode | None:
        """
        Retrieves a promo code by its code.

        Parameters
        ----------
        code : str
            The unique code of the promo code to retrieve.

        Returns
        -------
        DiscountPromoCode or None
            The promo code object if found, otherwise None.
        """
        if not code:
            return None

        return DiscountPromoCode.objects.filter(code=code).first()
