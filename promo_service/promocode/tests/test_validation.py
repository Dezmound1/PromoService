import pytest
from rest_framework.exceptions import ValidationError

from promocode.services import PromoCodeService


@pytest.mark.django_db
class TestPromoCodeValidation:
    """Test promo code validation against business rules."""

    def test_valid_promo(self, user, promo_universal) -> None:
        """Validate an active, non-expired promo code with remaining usages."""

        result = PromoCodeService.validate("TEST10", user.id)
        assert result.id == promo_universal.id

    def test_not_found(self, user) -> None:
        """Validate a promo code that does not exist in the database."""

        with pytest.raises(ValidationError, match="не найден"):
            PromoCodeService.validate("NOTEXIST", user.id)

    def test_expired(self, user, expired_promo) -> None:
        """Validate a promo code whose valid_until date is in the past."""

        with pytest.raises(ValidationError, match="просрочен"):
            PromoCodeService.validate("EXPIRED", user.id)

    def test_inactive(self, user, inactive_promo) -> None:
        """Validate a promo code with is_active=False."""

        with pytest.raises(ValidationError, match="неактивен"):
            PromoCodeService.validate("INACTIVE", user.id)

    def test_usage_limit_exhausted(self, user, exhausted_promo) -> None:
        """Validate a promo code that has reached its max_usages limit."""

        with pytest.raises(ValidationError, match="Лимит"):
            PromoCodeService.validate("ONEUSE", user.id)

    def test_already_used_by_user(self, user, promo_universal, existing_order) -> None:
        """Validate a promo code that the same user has already used."""

        with pytest.raises(ValidationError, match="использовали"):
            PromoCodeService.validate("TEST10", user.id)


@pytest.mark.django_db
class TestDiscountApplicability:
    """Test whether a discount applies to a specific good."""

    def test_applicable(self, good_game, promo_universal) -> None:
        """Check discount for an eligible good with a universal promo code."""

        assert (
            PromoCodeService.is_discount_applicable(good_game, promo_universal) is True
        )

    def test_not_eligible(self, good_no_promo, promo_universal) -> None:
        """Check discount for a good with promo_eligible=False."""

        assert (
            PromoCodeService.is_discount_applicable(good_no_promo, promo_universal)
            is False
        )

    def test_category_mismatch(self, good_vpn, promo_game) -> None:
        """Check discount for a good whose category does not match allowed_category."""

        assert PromoCodeService.is_discount_applicable(good_vpn, promo_game) is False

    def test_category_match(self, good_game, promo_game) -> None:
        """Check discount for a good whose category matches allowed_category."""

        assert PromoCodeService.is_discount_applicable(good_game, promo_game) is True
