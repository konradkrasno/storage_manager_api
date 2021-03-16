from django.db import models
from products.models import Product


class Image(models.Model):
    image = models.ImageField(upload_to="media/images/%Y/%m/%d")
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
