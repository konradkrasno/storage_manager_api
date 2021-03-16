from django.contrib import admin
from .models import Worker


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "position", "active"]
