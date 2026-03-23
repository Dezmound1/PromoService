from decimal import Decimal

import pytest

from orders.models import Order


@pytest.mark.django_db
class TestCreateOrderSuccess:
    """Test successful order creation scenarios."""

    def test_without_promo(self, api_client, user, good_game) -> None:
        """Create an order without a promo code."""

        response = api_client.post(
            "/orders/",
            {"user_id": user.id, "goods": [{"good_id": good_game.id, "quantity": 2}]},
            format="json",
        )

        assert response.status_code == 201
        assert Decimal(response.data["total"]) == Decimal("2000.00")
        assert Order.objects.count() == 1

    def test_with_promo(self, api_client, user, good_game, promo_universal) -> None:
        """Create an order with a valid universal promo code."""

        response = api_client.post(
            "/orders/",
            {
                "user_id": user.id,
                "goods": [{"good_id": good_game.id, "quantity": 1}],
                "promo_code": "TEST10",
            },
            format="json",
        )

        assert response.status_code == 201
        assert Decimal(response.data["price"]) == Decimal("1000.00")
        assert Decimal(response.data["total"]) == Decimal("900.00")

    def test_promo_not_applied_to_excluded_good(
        self, api_client, user, good_no_promo, promo_universal
    ) -> None:
        """Create an order with a promo code for a non-eligible good."""

        response = api_client.post(
            "/orders/",
            {
                "user_id": user.id,
                "goods": [{"good_id": good_no_promo.id, "quantity": 1}],
                "promo_code": "TEST10",
            },
            format="json",
        )

        assert response.status_code == 201
        assert Decimal(response.data["total"]) == Decimal("500.00")

    def test_promo_category_mismatch_no_discount(
        self, api_client, user, good_vpn, promo_game
    ) -> None:
        """Create an order with a category-restricted promo code on a mismatched good."""

        response = api_client.post(
            "/orders/",
            {
                "user_id": user.id,
                "goods": [{"good_id": good_vpn.id, "quantity": 1}],
                "promo_code": "GAME20",
            },
            format="json",
        )

        assert response.status_code == 201
        assert Decimal(response.data["total"]) == Decimal("2000.00")


@pytest.mark.django_db
class TestCreateOrderValidation:
    """Test input validation for order creation."""

    def test_missing_user_id(self, api_client, good_game):
        """Send a request without user_id field."""

        response = api_client.post(
            "/orders/",
            {"goods": [{"good_id": good_game.id, "quantity": 1}]},
            format="json",
        )
        assert response.status_code == 400

    def test_empty_goods(self, api_client, user):
        """Send a request with an empty goods list."""

        response = api_client.post(
            "/orders/",
            {"user_id": user.id, "goods": []},
            format="json",
        )
        assert response.status_code == 400

    def test_nonexistent_user(self, api_client, good_game):
        """Send a request with a user_id that does not exist in the database."""

        response = api_client.post(
            "/orders/",
            {"user_id": 99999, "goods": [{"good_id": good_game.id, "quantity": 1}]},
            format="json",
        )
        assert response.status_code == 400

    def test_nonexistent_good(self, api_client, user):
        """Send a request with a good_id that does not exist in the database."""

        response = api_client.post(
            "/orders/",
            {"user_id": user.id, "goods": [{"good_id": 99999, "quantity": 1}]},
            format="json",
        )
        assert response.status_code == 400
