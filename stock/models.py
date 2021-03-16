from django.db import models
from products.models import Product


class Stock(models.Model):
    """
    Assigns products to Shops or Stores.
    """


class StockPosition(models.Model):
    """
    Stores information about Product in Stock.
    """

    product = models.ForeignKey(
        Product, related_name="stock_positions", on_delete=models.CASCADE
    )
    stock = models.ForeignKey(Stock, related_name="positions", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    minimal_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    average_supply_time = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
