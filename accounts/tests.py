from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import CustomerProfile


class CustomerProfileModelTests(TestCase):
    def test_profile_creation(self):
        user = get_user_model().objects.create_user(username="alice")
        profile = CustomerProfile.objects.create(user=user, city="Dhaka", country="Bangladesh")
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.city, "Dhaka")
