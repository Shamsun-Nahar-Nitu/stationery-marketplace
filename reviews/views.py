from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Review


@login_required
@require_POST
def upsert_review(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    try:
        rating = int(request.POST.get("rating", 5))
    except (TypeError, ValueError):
        rating = 5

    if rating < 1 or rating > 5:
        messages.error(request, "Rating must be between 1 and 5.")
        return redirect("catalog:product_detail", slug=product.slug)

    title = request.POST.get("title", "").strip()
    body = request.POST.get("body", "").strip()

    _, created = Review.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={
            "rating": rating,
            "title": title,
            "body": body,
            "is_approved": True,
        },
    )

    if created:
        messages.success(request, "Thanks! Your review has been added.")
    else:
        messages.success(request, "Your review has been updated.")

    return redirect("catalog:product_detail", slug=product.slug)
