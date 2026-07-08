from django.contrib import admin
from .models import ShippingMethod


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "fee", "estimated_days", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
