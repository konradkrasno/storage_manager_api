from django.contrib import admin
from .models import Payment, Receipt, Invoice, AdvanceInvoice


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = [
        "created",
        "updated",
        "note",
        "value_net",
        "tax_value",
        "value_gross",
    ]


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "created",
        "updated",
        "state",
        "supply_date",
        "maturity",
        "note",
        "worker",
        "value_net",
        "tax_value",
        "value_gross",
    ]


@admin.register(AdvanceInvoice)
class AdvanceInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "created",
        "updated",
        "state",
        "supply_date",
        "maturity",
        "note",
        "worker",
        "advance_value",
        "value_net",
        "tax_value",
        "value_gross",
        "rest_value_net",
        "rest_tax_value",
        "rest_value_gross",
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "paid",
        "created",
        "updated",
        "receipt",
        "invoice",
        "advance_invoice",
    ]
