from django.db import models
from notes.models import Note
from workers.models import Worker


class Bill(models.Model):
    """
    Provides bills for specific Notes.
    Bills are divided into Invoice and Receipts.
    """

    TYPE_CHOICES = (
        ("invoice", "Invoice"),
        ("receipt", "Receipt"),
    )
    STATE_CHOICES = (
        ("in_progress", "In Progress"),
        ("executed", "Executed"),
        ("delayed", "Delayed"),
        ("cancelled", "Canceled"),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    number = models.CharField(max_length=20, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES, default="in_progress"
    )
    adjustment = models.BooleanField()
    supply_date = models.DateField()
    note = models.OneToOneField(Note, related_name="bill", on_delete=models.PROTECT)
    worker = models.ForeignKey(
        Worker, related_name="bills", on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return f"<Bill: {self.number}>"


class Payment(models.Model):
    """
    Contains payment details for specific Bills.
    """

    TYPE_CHOICES = (
        ("cash", "Cash"),
        ("transfer", "Transfer"),
    )
    bill = models.OneToOneField(Bill, related_name="payment", on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    number = models.CharField(max_length=20, db_index=True)
    maturity = models.DateTimeField()
    paid = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<Payment: {self.number}>"
