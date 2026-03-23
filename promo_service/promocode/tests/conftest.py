from datetime import timedelta
from decimal import Decimal

import pytest
from django.utils import timezone

from orders.models import Order
from promocode.models import DiscountPromoCode
from users.models import User


@pytest.fixture
def expired_promo(db):
    return DiscountPromoCode.objects.create(
        code="EXPIRED",
        is_active=True,
        valid_until=timezone.now() - timedelta(days=1),
        max_usages=10,
        discount_percent=10,
    )


@pytest.fixture
def inactive_promo(db):
    return DiscountPromoCode.objects.create(
        code="INACTIVE",
        is_active=False,
        valid_until=timezone.now() + timedelta(days=7),
        max_usages=10,
        discount_percent=10,
    )


@pytest.fixture
def exhausted_promo(db, user, good_game):
    """Промокод с лимитом 1, уже использован другим юзером."""
    promo = DiscountPromoCode.objects.create(
        code="ONEUSE",
        is_active=True,
        valid_until=timezone.now() + timedelta(days=7),
        max_usages=1,
        discount_percent=10,
    )
    other_user = User.objects.create(
        username="other", email="other@example.com", password="pass"
    )
    order = Order.objects.create(
        user=other_user, total_price=Decimal("900"), promo_code=promo
    )
    order.goods.add(good_game)
    return promo
