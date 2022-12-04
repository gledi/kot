from django.db import models


class Product(models.Model):    # shop_product
    EUR = "EUR"
    USD = "USD"
    ALL = "ALL"
    CURRENCY_CHOICES = [
        (EUR, "€"),
        (USD, "$"),
        (ALL, "Lek")
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "products"
