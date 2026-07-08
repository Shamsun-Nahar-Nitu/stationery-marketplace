from django.shortcuts import get_object_or_404, render

from reviews.models import Review
from wishlist.models import WishlistItem
from .models import Product


def product_list(request):
    products = (
        Product.objects.select_related("seller", "category")
        .filter(is_active=True)
        .order_by("-created_at")
    )
    return render(request, "catalog/product_list.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("seller", "category").filter(is_active=True),
        slug=slug,
    )
    reviews = Review.objects.select_related("user").filter(product=product, is_approved=True)
    user_review = None
    is_in_wishlist = False

    if request.user.is_authenticated:
        user_review = Review.objects.filter(product=product, user=request.user).first()
        is_in_wishlist = WishlistItem.objects.filter(product=product, user=request.user).exists()

    return render(
        request,
        "catalog/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "user_review": user_review,
            "is_in_wishlist": is_in_wishlist,
        },
    )