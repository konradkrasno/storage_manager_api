from django.contrib import admin
from .models import Manufacturer, Category, Product


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "group",
        "code",
        "batch_number",
        "unit",
        "purchase_price",
        "sales_price_net",
        "tax_rate",
        "best_before_date",
        "description",
        "created",
        "updated",
        "manufacturer",
        "category",
    ]
