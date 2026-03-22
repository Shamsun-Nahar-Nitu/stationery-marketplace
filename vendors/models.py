from django.conf import settings
from django.db import models


class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_profile")
    store_name = models.CharField(max_length=120, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.store_name