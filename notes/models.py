from decimal import Decimal

from django.db import models
from products.models import Product
from stock.models import Stock
from workers.models import Worker
from accounts.models import User


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
    company_name = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    user = models.ForeignKey(User, related_name="contractors", on_delete=models.CASCADE)

    def __str__(self):
        return f"<Contractor: {self.user.first_name} {self.user.last_name}>"


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
        ("return", "Return"),
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
        null=True,
    )
    from_shop = models.ForeignKey(
        Shop,
        related_name="dispatch_notes",
        on_delete=models.PROTECT,
        null=True,
    )
    from_contractor = models.ForeignKey(
        Contractor,
        related_name="dispatch_notes",
        on_delete=models.PROTECT,
        null=True,
    )
    to_store = models.ForeignKey(
        Store,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        null=True,
    )
    to_shop = models.ForeignKey(
        Shop,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        null=True,
    )
    to_contractor = models.ForeignKey(
        Contractor,
        related_name="supply_notes",
        on_delete=models.PROTECT,
        null=True,
    )
    worker = models.ForeignKey(
        Worker, related_name="notes", on_delete=models.PROTECT, blank=True, null=True
    )
    value_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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
    price_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.PositiveIntegerField(default=0)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"<NotePosition: {self.product}>"

    def save(self, *args, **kwargs):
        if self.price_net:
            self.calculate_position_values()
            self.calculate_note_values()
        super().save(*args, **kwargs)

    def calculate_position_values(self):
        """
        Calculates value_net, tax_value and value_gross for NotePosition.
        """

        discounted_price = Decimal(self.price_net) - Decimal(self.discount_value)
        self.value_net = discounted_price * Decimal(self.quantity)
        self.tax_value = self.value_net * Decimal(self.tax_rate) / 100
        self.value_gross = self.value_net + self.tax_value

    def calculate_note_values(self):
        """
        Updates value_net, tax_value and value_gross in related Note.
        """

        value_net = Decimal(self.note.value_net)
        value_net += Decimal(self.value_net)
        self.note.value_net = value_net

        tax_value = Decimal(self.note.tax_value)
        tax_value += Decimal(self.tax_value)
        self.note.tax_value = tax_value

        value_gross = Decimal(self.note.value_gross)
        value_gross += Decimal(self.value_gross)
        self.note.value_gross = value_gross

        self.note.save()
