from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import WishlistItem


@login_required
def wishlist_detail(request):
    items = (
        WishlistItem.objects.select_related("product", "product__seller", "product__category")
        .filter(user=request.user, product__is_active=True)
        .order_by("-created_at")
    )
    return render(request, "wishlist/detail.html", {"items": items})


@login_required
@require_POST
def wishlist_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    _, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f"'{product.name}' added to your wishlist.")
    else:
        messages.info(request, f"'{product.name}' is already in your wishlist.")
    return redirect("catalog:product_detail", slug=product.slug)


@login_required
@require_POST
def wishlist_remove(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    deleted, _ = WishlistItem.objects.filter(user=request.user, product=product).delete()
    if deleted:
        messages.success(request, f"'{product.name}' removed from your wishlist.")
    else:
        messages.info(request, f"'{product.name}' was not in your wishlist.")
    return redirect("catalog:product_detail", slug=product.slug)
