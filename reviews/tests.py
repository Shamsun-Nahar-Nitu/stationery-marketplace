from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Product
from vendors.models import SellerProfile
from .models import Review


class ReviewViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="buyer")
        self.seller_user = user_model.objects.create_user(username="seller")
        self.seller = SellerProfile.objects.create(user=self.seller_user, store_name="Bravo Store")
        self.product = Product.objects.create(
            seller=self.seller,
            name="Pen",
            price="2.50",
            stock=20,
            is_active=True,
        )

    def test_upsert_review_requires_login(self):
        url = reverse("reviews:upsert", args=[self.product.id])
        response = self.client.post(url, {"rating": 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_logged_in_user_can_create_and_update_review(self):
        self.client.force_login(self.user)
        url = reverse("reviews:upsert", args=[self.product.id])

        self.client.post(url, {"rating": 4, "title": "Good", "body": "Nice quality"})
        review = Review.objects.get(user=self.user, product=self.product)
        self.assertEqual(review.rating, 4)

        self.client.post(url, {"rating": 5, "title": "Great", "body": "Excellent"})
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(Review.objects.filter(user=self.user, product=self.product).count(), 1)
