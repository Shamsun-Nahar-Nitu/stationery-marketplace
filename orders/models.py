from django.conf import settings
from django.db import models


class Order(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=10, decimal_places=2, default="0.00")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product_name} x{self.quantity}"