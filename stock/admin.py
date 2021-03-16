from django.contrib import admin
from .models import Stock, StockPosition


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(StockPosition)
class StockPositionAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "quantity",
        "minimal_quantity",
        "average_supply_time",
        "stock",
    ]
