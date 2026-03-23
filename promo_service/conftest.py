from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from goods.models import Good
from orders.models import Order
from promocode.models import DiscountPromoCode
from users.models import User


@pytest.fixture
def user(db):
    return User.objects.create(
        username="testuser",
        email="test@example.com",
        password="testpass",
    )


@pytest.fixture
def good_game(db):
    return Good.objects.create(
        name="Test Game",
        price=Decimal("1000.00"),
        count=10,
        category=Good.Status.GAME,
        promo_eligible=True,
    )


@pytest.fixture
def good_vpn(db):
    return Good.objects.create(
        name="VPN Service",
        price=Decimal("2000.00"),
        count=100,
        category=Good.Status.VPN,
        promo_eligible=True,
    )


@pytest.fixture
def good_no_promo(db):
    return Good.objects.create(
        name="Exclusive Item",
        price=Decimal("500.00"),
        count=5,
        category=Good.Status.GAME,
        promo_eligible=False,
    )


@pytest.fixture
def promo_universal(db):
    return DiscountPromoCode.objects.create(
        code="TEST10",
        is_active=True,
        valid_until=timezone.now() + timedelta(days=7),
        max_usages=10,
        discount_percent=10,
        allowed_category=None,
    )


@pytest.fixture
def promo_game(db):
    return DiscountPromoCode.objects.create(
        code="GAME20",
        is_active=True,
        valid_until=timezone.now() + timedelta(days=7),
        max_usages=10,
        discount_percent=20,
        allowed_category=Good.Status.GAME,
    )


@pytest.fixture
def existing_order(user, good_game, promo_universal):
    """Order that already used promo_universal."""
    order = Order.objects.create(
        user=user,
        total_price=Decimal("900.00"),
        promo_code=promo_universal,
    )
    order.goods.add(good_game)
    return order
