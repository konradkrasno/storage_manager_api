import csv
from datetime import datetime, timedelta
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from notes.models import Note
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from test_data import test_data
from workers.models import Worker

from .models import Payment, Receipt, Invoice, AdvanceInvoice
from .permissions import IsWorker
from .serializers import ReceiptSerializer, InvoiceSerializer, AdvanceInvoiceSerializer


class AddTestData(APIView):
    def post(self, request):
        """Adds test data to the database."""

        if not Note.objects.first():
            for model, values in test_data.items():
                for data in values:
                    model(**data).save()
            return Response({"ok": "Test data uploaded"})
        else:
            return Response({"ok": "Test data uploaded already"})


class ReceiptListView(generics.ListAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer


class InvoiceListView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class AdvanceInvoiceListView(generics.ListAPIView):
    queryset = AdvanceInvoice.objects.all()
    serializer_class = AdvanceInvoiceSerializer


class ReceiptDetailView(generics.RetrieveAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    lookup_field = "note__number"


class InvoiceDetailView(generics.RetrieveAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = "note__number"


class AdvanceInvoiceDetailView(generics.RetrieveAPIView):
    queryset = AdvanceInvoice.objects.all()
    serializer_class = AdvanceInvoiceSerializer
    lookup_field = "note__number"


class ReceiptCreateView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def post(self, request, note_number):
        note = get_object_or_404(
            Note, number=note_number, type="dispatch", handover_type="external"
        )
        if hasattr(note, "receipt"):
            return Response({"error": "Receipt has been already created"})
        elif hasattr(note, "advance_invoice"):
            return Response({"error": "Advance invoice has been already created"})

        Receipt(note=note).save()
        receipt = Receipt.objects.get(note__number=note_number)
        try:
            payment = Payment.objects.get(note_id=note.id)
        except Payment.DoesNotExist:
            Payment(receipt=receipt, note=note).save()
        else:
            payment.receipt = receipt
            payment.save()
        return Response({"created": True})


class InvoiceCreateView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def post(self, request, note_number, worker_id, supply_time):
        note = get_object_or_404(
            Note, number=note_number, type="dispatch", handover_type="external"
        )
        if hasattr(note, "invoice"):
            return Response(
                {"error": "Invoice for given note has been already created"}
            )

        worker = get_object_or_404(Worker, id=worker_id)
        Invoice(
            note=note,
            worker=worker,
            supply_date=datetime.utcnow() + timedelta(days=supply_time),
        ).save()
        invoice = Invoice.objects.get(note__number=note_number)
        try:
            payment = Payment.objects.get(note_id=note.id)
        except Payment.DoesNotExist:
            Payment(invoice=invoice, note=note).save()
        else:
            payment.invoice = invoice
            payment.save()
        return Response({"created": True})


class AdvanceInvoiceCreateView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def post(self, request, note_number, worker_id, supply_time, advance_value):
        note = get_object_or_404(
            Note, number=note_number, type="dispatch", handover_type="external"
        )
        if hasattr(note, "receipt"):
            return Response(
                {"error": "Receipt for given note has been already created"}
            )
        elif hasattr(note, "invoice"):
            return Response(
                {"error": "Invoice for given note has been already created"}
            )
        elif hasattr(note, "advance_invoice"):
            return Response(
                {"error": "Advance invoice for given note has been already created"}
            )

        worker = get_object_or_404(Worker, id=worker_id)
        AdvanceInvoice(
            note=note,
            worker=worker,
            supply_date=datetime.utcnow() + timedelta(days=supply_time),
            advance_value=advance_value,
        ).save()
        adv_invoice = AdvanceInvoice.objects.get(note__number=note_number)
        Payment(advance=True, advance_invoice=adv_invoice, note=note).save()
        return Response({"created": True})


class InvoiceUpdateView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def put(self, request, note_number, worker_id, supply_time, state):
        worker = get_object_or_404(Worker, id=worker_id)
        invoice = get_object_or_404(Invoice, note__number=note_number)
        invoice.state = state
        invoice.worker = worker
        invoice.supply_date = datetime.utcnow() + timedelta(days=supply_time)
        invoice.save()
        return Response({"updated": True})


class AdvanceInvoiceUpdateView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def put(self, request, note_number, worker_id, supply_time, state, advance_value):
        worker = get_object_or_404(Worker, id=worker_id)
        invoice = get_object_or_404(AdvanceInvoice, note__number=note_number)
        invoice.state = state
        invoice.worker = worker
        invoice.supply_date = datetime.utcnow() + timedelta(days=supply_time)
        invoice.advance_value = Decimal(advance_value)
        invoice.save()
        return Response({"updated": True})


class ReceiptDeleteView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def delete(self, request, note_number):
        Receipt.objects.filter(note__number=note_number).delete()
        return Response({"deleted": True})


class InvoiceDeleteView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def delete(self, request, note_number):
        Invoice.objects.filter(note__number=note_number).delete()
        return Response({"deleted": True})


class AdvanceInvoiceDeleteView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsWorker,)

    def delete(self, request, note_number):
        AdvanceInvoice.objects.filter(note__number=note_number).delete()
        return Response({"deleted": True})


class ExportData(APIView):
    def get(self, request, note_number=None):
        if note_number:
            notes = Note.objects.filter(number=note_number).all()
        else:
            notes = Note.objects.filter(type="dispatch", handover_type="external").all()
        rows = self.prepare_data_to_csv(notes)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        [writer.writerow(row) for row in rows]
        return response

    @property
    def fields(self):
        return [
            "marketplace",
            "country",
            "invoice_id",
            "transaction_id",
            "transaction_time",
            "transaction_type",
            "item_name",
            "item_type",
            "units",
            "marketplace_currency",
            "sales_price",
            "estimated_earnings",
            "client_id",
            "receipt_id",
        ]

    def prepare_data_to_csv(self, notes):
        rows = [self.fields]
        for note in notes:
            for item in note.positions.all():
                from_entity = note.from_store if note.from_store else note.from_shop
                row = [
                    from_entity.city,
                    "PL",
                    note.invoice.id if hasattr(note, "invoice") else None,
                    note.number,
                    note.updated,
                    note.type,
                    item.product.name,
                    item.product.category.name,
                    item.product.unit,
                    "PLN",
                    item.price_net,
                    item.price_net - item.product.purchase_price,
                    note.to_contractor.id,
                    note.receipt.id if hasattr(note, "receipt") else None,
                ]
                rows.append(row)
        return rows
