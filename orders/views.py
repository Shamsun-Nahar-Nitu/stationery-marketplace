from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Order, OrderItem



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def checkout(request):
    cart = _get_cart(request.session)
    items, total = _build_cart_items(cart)

    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "total": total,
        },
    )


@login_required
@require_POST
def place_order(request):
    cart = _get_cart(request.session)
    items, total = _build_cart_items(cart)

    if not items:
        return redirect("cart:detail")

    with transaction.atomic():
        order = Order.objects.create(user=request.user, status=Order.STATUS_PENDING)

        for item in items:
            product = item["product"]
            qty = item["qty"]

            updated = (
                Product.objects.filter(id=product.id, stock__gte=qty)
                .update(stock=F("stock") - qty)
            )
            if updated != 1:
                raise Http404("Not enough stock to place this order. Please update your cart.")

            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                unit_price=product.price,
                quantity=qty,
            )

        request.session["cart"] = {}
        request.session.modified = True

    return redirect("orders:detail", order_id=order.id)
