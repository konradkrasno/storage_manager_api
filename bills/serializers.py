from accounts.models import User
from notes.models import Note, NotePosition, Contractor
from products.models import Product
from rest_framework import serializers
from workers.models import Worker

from .models import Receipt, Invoice, AdvanceInvoice


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Worker
        fields = ["user", "position"]


class ContractorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Contractor
        fields = [
            "user",
            "company_name",
            "address",
            "postal_code",
            "city",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "unit"]


class NotePositionSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = NotePosition
        fields = [
            "product",
            "quantity",
            "price_net",
            "tax_rate",
            "discount_value",
            "value_net",
            "tax_value",
            "value_gross",
        ]


class NoteSerializer(serializers.ModelSerializer):
    positions = NotePositionSerializer(many=True, read_only=True)
    to_contractor = ContractorSerializer(read_only=True)

    class Meta:
        model = Note
        fields = [
            "number",
            "to_contractor",
            "positions",
            "value_net",
            "tax_value",
            "value_gross",
        ]


class ReceiptSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = Receipt
        exclude = ["id"]


class InvoiceSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = Invoice
        exclude = ["id"]


class AdvanceInvoiceSerializer(serializers.ModelSerializer):
    worker = WorkerSerializer(read_only=True)
    note = NoteSerializer(read_only=True)

    class Meta:
        model = AdvanceInvoice
        exclude = [
            "id",
            "advance_value",
            "rest_value_net",
            "rest_tax_value",
            "rest_value_gross",
        ]
