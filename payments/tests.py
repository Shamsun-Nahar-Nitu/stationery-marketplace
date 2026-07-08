from django.test import TestCase
from django.contrib.auth import get_user_model

from orders.models import Order
from .models import Payment


class PaymentModelTests(TestCase):
    def test_payment_creation(self):
        user = get_user_model().objects.create_user(username="buyer")
        order = Order.objects.create(user=user)
        payment = Payment.objects.create(order=order, amount="99.50", currency="USD")
        self.assertEqual(payment.order, order)
        self.assertEqual(payment.status, Payment.STATUS_PENDING)
