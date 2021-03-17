from datetime import datetime, timedelta
from decimal import Decimal

from django.db import models
from notes.models import Note
from workers.models import Worker


class Receipt(models.Model):
    """
    Provides Receipt for specific Notes.
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    note = models.OneToOneField(Note, related_name="receipt", on_delete=models.PROTECT)
    value_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"<Receipt: {self.id}>"

    def save(self, *args, **kwargs):
        self.value_net = self.note.value_net
        self.tax_value = self.note.tax_value
        self.value_gross = self.note.value_gross
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """
    Provides Invoice for specific Notes.
    """

    STATE_CHOICES = (
        ("in_progress", "In Progress"),
        ("executed", "Executed"),
        ("delayed", "Delayed"),
        ("cancelled", "Canceled"),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default="in_progress"
    )
    supply_date = models.DateField(default=datetime.utcnow)
    maturity = models.DateField(default=datetime.today() + timedelta(days=30))
    note = models.OneToOneField(Note, related_name="invoice", on_delete=models.PROTECT)
    worker = models.ForeignKey(
        Worker, related_name="invoices", on_delete=models.PROTECT
    )
    value_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"<Invoice: {self.id}>"

    def save(self, *args, **kwargs):
        if hasattr(self.note, "advance_invoice"):
            self.value_net = self.note.advance_invoice.rest_value_net
            self.tax_value = self.note.advance_invoice.rest_tax_value
            self.value_gross = self.note.advance_invoice.rest_value_gross
        else:
            self.value_net = self.note.value_net
            self.tax_value = self.note.tax_value
            self.value_gross = self.note.value_gross
        super().save(*args, **kwargs)


class AdvanceInvoice(models.Model):
    """
    Provides Invoice with advance payment for specific Notes.
    """

    STATE_CHOICES = (
        ("in_progress", "In Progress"),
        ("executed", "Executed"),
        ("delayed", "Delayed"),
        ("cancelled", "Canceled"),
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default="in_progress"
    )
    supply_date = models.DateField(default=datetime.utcnow)
    maturity = models.DateField(default=datetime.today() + timedelta(days=30))
    note = models.OneToOneField(
        Note, related_name="advance_invoice", on_delete=models.PROTECT
    )
    worker = models.ForeignKey(
        Worker, related_name="advance_invoices", on_delete=models.PROTECT
    )
    advance_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_net = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_gross = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rest_value_net = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rest_tax_value = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rest_value_gross = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"<AdvanceInvoices: {self.id}>"

    def save(self, *args, **kwargs):
        if self.note.value_gross:
            self.calculate_advance_values()
            self.calculate_rest_values()
        super().save(*args, **kwargs)

    def calculate_advance_values(self):
        self.tax_value = (
            Decimal(self.advance_value)
            * Decimal(self.note.tax_value)
            / Decimal(self.note.value_gross)
        )
        self.value_net = Decimal(self.advance_value) - self.tax_value
        self.value_gross = Decimal(self.advance_value)

    def calculate_rest_values(self):
        self.rest_value_net = Decimal(self.note.value_net) - self.value_net
        self.rest_tax_value = Decimal(self.note.tax_value) - self.tax_value
        self.rest_value_gross = self.rest_value_net + self.rest_tax_value


class Payment(models.Model):
    """
    Contains payment details for specific Bills.
    """

    TYPE_CHOICES = (
        ("cash", "Cash"),
        ("transfer", "Transfer"),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, null=True)
    advance = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    receipt = models.OneToOneField(
        Receipt, related_name="receipt_payment", on_delete=models.CASCADE, null=True
    )
    invoice = models.OneToOneField(
        Invoice, related_name="invoice_payment", on_delete=models.CASCADE, null=True
    )
    advance_invoice = models.OneToOneField(
        AdvanceInvoice,
        related_name="advance_invoice_payment",
        on_delete=models.CASCADE,
        null=True,
    )
    note = models.ForeignKey(Note, related_name="payments", on_delete=models.CASCADE)

    def __str__(self):
        return f"<Payment: {self.id}>"
