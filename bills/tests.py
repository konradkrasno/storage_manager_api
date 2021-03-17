from datetime import date, timedelta
from decimal import Decimal

import pytest
from bills.models import AdvanceInvoice, Invoice, Receipt
from notes.models import Note


@pytest.mark.django_db
class TestModels:

    @staticmethod
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

    @staticmethod
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


@pytest.mark.django_db
class TestViews:

    @staticmethod
    def test_receipt_create_view(client):
        assert not Receipt.objects.first()
        response = client.post("/bills/receipts/create/EXT-DIS-1/")
        assert response.status_code == 200
        receipt = Receipt.objects.first()
        assert receipt.value_net == Decimal("95.70")
        assert receipt.tax_value == Decimal("22.01")
        assert receipt.value_gross == Decimal("117.71")

    @staticmethod
    def test_invoice_create_view(client):
        assert not Invoice.objects.first()
        response = client.post("/bills/invoices/create/EXT-DIS-1/1/3/")
        assert response.status_code == 200
        invoice = Invoice.objects.first()
        assert invoice.worker.id == 1
        assert invoice.state == "in_progress"
        assert invoice.supply_date == date.today() + timedelta(days=3)
        assert invoice.maturity == date.today() + timedelta(days=30)
        assert invoice.value_net == Decimal("95.70")
        assert invoice.tax_value == Decimal("22.01")
        assert invoice.value_gross == Decimal("117.71")

    @staticmethod
    def test_advance_invoice_create_view(client):
        assert not AdvanceInvoice.objects.first()
        response = client.post("/bills/adv_invoices/create/EXT-DIS-1/1/3/50/")
        assert response.status_code == 200
        invoice = AdvanceInvoice.objects.first()
        assert invoice.worker.id == 1
        assert invoice.state == "in_progress"
        assert invoice.supply_date == date.today() + timedelta(days=3)
        assert invoice.maturity == date.today() + timedelta(days=30)
        assert invoice.value_net == Decimal("40.65")
        assert invoice.tax_value == Decimal("9.35")
        assert invoice.value_gross == Decimal("50.00")
        assert invoice.rest_value_net == Decimal("55.05")
        assert invoice.rest_tax_value == Decimal("12.66")
        assert invoice.rest_value_gross == Decimal("67.71")

    @staticmethod
    def test_invoice_update_view(client):
        client.post("/bills/invoices/create/EXT-DIS-1/1/3/")
        response = client.put("/bills/invoices/update/EXT-DIS-1/2/5/executed/")
        assert response.status_code == 200
        invoice = Invoice.objects.first()
        assert invoice.worker.id == 2
        assert invoice.state == "executed"
        assert invoice.supply_date == date.today() + timedelta(days=5)

    @staticmethod
    def test_advance_invoice_update_view(client):
        client.post("/bills/adv_invoices/create/EXT-DIS-1/1/3/50/")
        response = client.put("/bills/adv_invoices/update/EXT-DIS-1/2/5/executed/40/")
        assert response.status_code == 200
        invoice = AdvanceInvoice.objects.first()
        assert invoice.worker.id == 2
        assert invoice.state == "executed"
        assert invoice.supply_date == date.today() + timedelta(days=5)
        assert invoice.value_net == Decimal("32.52")
        assert invoice.tax_value == Decimal("7.48")
        assert invoice.value_gross == Decimal("40.00")
        assert invoice.rest_value_net == Decimal("63.18")
        assert invoice.rest_tax_value == Decimal("14.53")
        assert invoice.rest_value_gross == Decimal("77.71")

    @staticmethod
    @pytest.mark.django_db
    def test_receipt_delete_view(client):
        client.post("/bills/receipts/create/EXT-DIS-1/")
        assert Receipt.objects.first()
        response = client.delete("/bills/receipts/delete/EXT-DIS-1/")
        assert response.status_code == 200
        assert not Receipt.objects.first()

    @staticmethod
    @pytest.mark.django_db
    def test_invoice_delete_view(client):
        client.post("/bills/invoices/create/EXT-DIS-1/1/3/")
        assert Invoice.objects.first()
        response = client.delete("/bills/invoices/delete/EXT-DIS-1/")
        assert response.status_code == 200
        assert not Invoice.objects.first()

    @staticmethod
    @pytest.mark.django_db
    def test_advance_invoice_delete_view(client):
        client.post("/bills/adv_invoices/create/EXT-DIS-1/1/3/50/")
        assert AdvanceInvoice.objects.first()
        response = client.delete("/bills/adv_invoices/delete/EXT-DIS-1/")
        assert response.status_code == 200
        assert not AdvanceInvoice.objects.first()
