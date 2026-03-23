from .models import DiscountPromoCode


class PromoCodeRepository:
    """Repository class for accessing promo code data."""

    @staticmethod
    def get_by_code(code: str) -> DiscountPromoCode | None:
        """
        Retrieve a promo code by its code string.

        Parameters
        ----------
        code : str
            The code string of the promo code to retrieve.

        Returns
        -------
        DiscountPromoCode | None
            The promo code instance if found, otherwise None.
        """
        return DiscountPromoCode.objects.filter(code=code).first()
