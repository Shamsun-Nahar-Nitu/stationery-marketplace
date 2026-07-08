from django.db import models


class ShippingMethod(models.Model):
    name = models.CharField(max_length=120, unique=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2)
    estimated_days = models.PositiveIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fee", "name"]

    def __str__(self) -> str:
        return f"{self.name} (${self.fee})"
