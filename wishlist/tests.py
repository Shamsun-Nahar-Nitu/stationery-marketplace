from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from catalog.models import Product
from vendors.models import SellerProfile
from .models import WishlistItem


class WishlistViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username="buyer")
        self.seller_user = user_model.objects.create_user(username="seller")
        self.seller = SellerProfile.objects.create(user=self.seller_user, store_name="Alpha Store")
        self.product = Product.objects.create(
            seller=self.seller,
            name="Notebook",
            price="10.00",
            stock=10,
            is_active=True,
        )

    def test_add_to_wishlist_requires_login(self):
        url = reverse("wishlist:add", args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(WishlistItem.objects.count(), 0)

    def test_logged_in_user_can_add_and_remove(self):
        self.client.force_login(self.user)
        add_url = reverse("wishlist:add", args=[self.product.id])
        remove_url = reverse("wishlist:remove", args=[self.product.id])

        self.client.post(add_url)
        self.assertTrue(WishlistItem.objects.filter(user=self.user, product=self.product).exists())

        self.client.post(remove_url)
        self.assertFalse(WishlistItem.objects.filter(user=self.user, product=self.product).exists())
