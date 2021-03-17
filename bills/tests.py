from decimal import Decimal

import pytest
from bills.models import AdvanceInvoice, Invoice
from notes.models import Note


@pytest.mark.django_db
def test_create_invoice():
    note = Note.objects.get(number="EXT-DIS-1")
    Invoice(
        note=note,
        worker_id=1,
    ).save()
    bill = Invoice.objects.latest("id")
    assert bill.value_net == Decimal("95.70")
    assert bill.tax_value == Decimal("22.01")
    assert bill.value_gross == Decimal("117.71")


@pytest.mark.django_db
def test_create_advance_invoice():
    adv_note = Note.objects.get(number="EXT-DIS-1")
    AdvanceInvoice(
        state="in_progress",
        advance_value=50,
        note=adv_note,
        worker_id=1,
    ).save()
    bill = AdvanceInvoice.objects.latest("id")
    assert bill.value_net == Decimal("40.65")
    assert bill.tax_value == Decimal("9.35")
    assert bill.value_gross == Decimal("50.00")
    assert bill.rest_value_net == Decimal("55.05")
    assert bill.rest_tax_value == Decimal("12.66")
    assert bill.rest_value_gross == Decimal("67.71")

    note = Note.objects.get(number="EXT-DIS-1")
    Invoice(
        note=note,
        worker_id=1,
    ).save()
    bill = Invoice.objects.latest("id")
    assert bill.value_net == Decimal("55.05")
    assert bill.tax_value == Decimal("12.66")
    assert bill.value_gross == Decimal("67.71")
