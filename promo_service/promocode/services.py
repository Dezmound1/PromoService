from datetime import timezone
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError

from promo_service.promocode.repository import PromoCodeRepository
from promo_service.users.repository import UserRepository


class PromoCodeService:
    """Service class for handling promo code related operations."""

    def __init__(self, request: Request):
        self.request = request.POST
        self.promo_code_repository = PromoCodeRepository()
        self.user_repository = UserRepository()
        self.promo_code = self.promo_code_repository.get_promo_code(
            self.request.get("promocode", "")
        )

    def promocode_validation(self) -> bool:
        """Validates the provided promo code."""

        if not self.promo_code:
            return False

        if self.usage_limit_validation():
            raise ValidationError("This promo code has reached its usage limit.")

        if not self.expired_validation():
            raise ValidationError("This promo code has expired.")

        return True

    def expired_validation(self) -> bool:
        """Checks if the promo code has expired."""
        return self.promo_code.valid_until < timezone.now()

    def usage_limit_validation(self) -> bool:
        """Checks if the promo code has remaining usages available."""
        return self.promo_code.usages < 1

    def user_eligibility_validation(self) -> bool:
        """Checks if the user is eligible to use the promo code."""
        # user = self.user_repository.get_user(self.request.get("user_id", 0))

        ...
