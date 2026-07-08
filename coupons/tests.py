from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Coupon


class CouponModelTests(TestCase):
    def test_coupon_validity_window(self):
        now = timezone.now()
        coupon = Coupon.objects.create(
            code="SAVE10",
            discount_percent=10,
            is_active=True,
            valid_from=now - timedelta(days=1),
            valid_to=now + timedelta(days=1),
        )
        self.assertTrue(coupon.is_valid_now())
