from django.db import models


class Order(models.Model):
    """Model representing a customer order."""

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="orders"
    )
    goods = models.ManyToManyField("goods.Good", related_name="orders")
    promo_code = models.ForeignKey(
        "promocode.DiscountPromoCode",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
