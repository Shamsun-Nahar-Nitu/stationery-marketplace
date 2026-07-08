from django.test import TestCase

from .models import ShippingMethod


class ShippingMethodModelTests(TestCase):
    def test_str(self):
        method = ShippingMethod.objects.create(name="Standard", fee="5.00", estimated_days=5)
        self.assertIn("Standard", str(method))
