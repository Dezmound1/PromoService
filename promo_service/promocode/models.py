from datetime import timedelta, datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from goods.models import Good


def default_valid_until():
    """Returns a default expiration date 14 days from now."""

    return datetime.now() + timedelta(days=14)


class BasePromoCode(models.Model):
    """Abstract base model for promo codes."""

    code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(default=default_valid_until)

    class Meta:
        abstract = True


class DiscountPromoCode(BasePromoCode):
    """A promo code that provides a percentage discount on the order total."""

    max_usages = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    discount_percent = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    allowed_category = models.CharField(
        choices=Good.Status.choices,
        null=True,
        blank=True,
        default=None,
    )
