from django.db import models


class Manufacturer(models.Model):
    """
    Provides the manufacturer of the Product.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"<Manufacturer: {self.name}>"


class Category(models.Model):
    """
    Provides the category of the Product.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"<Category: {self.name}>"


class Product(models.Model):
    """
    Provides product data.
    """

    GROUP_CHOICES = (
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
    )
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=2, choices=GROUP_CHOICES)
    code = models.CharField(max_length=50, db_index=True)
    batch_number = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sales_price_net = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.PositiveIntegerField()
    best_before_date = models.DateField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    manufacturer = models.ForeignKey(
        Manufacturer, related_name="products", on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"<Product: {self.name}>"
