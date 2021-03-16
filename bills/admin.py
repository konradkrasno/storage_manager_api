from django.contrib import admin
from .models import Payment, Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "number",
        "created",
        "updated",
        "state",
        "adjustment",
        "supply_date",
        "note",
        "worker",
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["bill", "type", "number", "maturity", "paid", "created", "updated"]
