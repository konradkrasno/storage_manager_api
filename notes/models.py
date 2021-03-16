from django.db import models
from products.models import Product
from stock.models import Stock
from workers.models import Worker


class Store(models.Model):
    """
    Provides data about the stores.
    """

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    stock = models.OneToOneField(Stock, related_name="store", on_delete=models.CASCADE)

    def __str__(self):
        return f"<Store: {self.name}>"


class Shop(models.Model):
    """
    Provides data about the shops.
    """

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    stock = models.OneToOneField(Stock, related_name="shop", on_delete=models.CASCADE)

    def __str__(self):
        return f"<Shop: {self.name}>"


class Contractor(models.Model):
    """
    Provides data about the contactors.
    Contractors are divided into groups: clients and suppliers.
    """

    TYPE_CHOICES = (
        ("client", "Client"),
        ("supplier", "Supplier"),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    company_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"<Contractor: {self.first_name} {self.last_name}>"


class Note(models.Model):
    """
    Note confirms the order, delivery, or dispatch of Products.
    Notes are used to calculate the stock of products in all Stores and Shops.
    Notes are the basis for invoicing.
    One Note can refer to only one entity 'from' and one entity 'to'.
    """

    TYPE_CHOICES = (
        ("order", "Order"),
        ("supply", "Supply"),
        ("dispatch", "Dispatch"),
    )
    HANDOVER_TYPE_CHOICES = (
        ("internal", "Internal"),
        ("external", "External"),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    handover_type = models.CharField(max_length=10, choices=HANDOVER_TYPE_CHOICES)
    number = models.CharField(max_length=20, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    from_store = models.ForeignKey(
        Store,
        related_name="dispatch_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    from_shop = models.ForeignKey(
        Shop,
        related_name="dispatch_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    from_contractor = models.ForeignKey(
        Contractor,
        related_name="dispatch_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    to_store = models.ForeignKey(
        Store,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    to_shop = models.ForeignKey(
        Shop,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    to_contractor = models.ForeignKey(
        Contractor,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    worker = models.ForeignKey(
        Worker, related_name="notes", on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return f"<Note: {self.number}>"


class NotePosition(models.Model):
    """
    Contains data on the quantity, the net price of the Product,
    the tax due and any discounts at the time the Note was created.
    """

    note = models.ForeignKey(Note, related_name="positions", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="note_positions", on_delete=models.PROTECT
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_net = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax_rate = models.PositiveIntegerField(null=True)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"<NotePosition: {self.product}>"
