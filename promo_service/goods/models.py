from django.db import models
from django.core.validators import MinValueValidator


class Good(models.Model):
    """Model representing a good that can be purchased."""

    class Status(models.TextChoices):
        """Enum for categorizing goods into different types."""

        ANOTHER = "another"
        GAME = "game"
        SKIN = "skin"
        VPN = "vpn"
        SUBSCRIPTION = "subscription"

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    count = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    category = models.CharField(
        max_length=50,
        choices=Status.choices,
        blank=True,
        default=Status.ANOTHER,
    )
    promo_eligible = models.BooleanField(default=True)
