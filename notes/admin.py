from django.contrib import admin

from .models import Store, Shop, Contractor, Note, NotePosition


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "postal_code", "city", "stock"]


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "postal_code", "city", "stock"]


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "first_name",
        "last_name",
        "company_name",
        "email",
        "address",
        "postal_code",
        "city",
    ]


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        "type",
        "handover_type",
        "number",
        "created",
        "updated",
        "from_store",
        "from_shop",
        "from_contractor",
        "to_store",
        "to_shop",
        "to_contractor",
        "worker",
    ]


@admin.register(NotePosition)
class NotePositionAdmin(admin.ModelAdmin):
    list_display = [
        "note",
        "product",
        "quantity",
        "price_net",
        "tax_rate",
        "discount_value",
    ]
