from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Order, OrderItem


def _get_cart(session):
    # same structure used in cart app
    cart = session.get("cart")
    if cart is None:
        cart = session["cart"] = {}
    return cart


def _build_cart_items(cart):
    """
    Returns (items, total) from session cart.
    items: list of dicts {product, qty, line_total}
    """
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.select_related("seller", "category").filter(id__in=product_ids, is_active=True)

    product_map = {p.id: p for p in products}

    items = []
    total = Decimal("0.00")

    for pid_str, data in cart.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if not product:
            continue

        qty = int(data.get("qty", 0))
        if qty <= 0:
            continue

        # Respect stock in display too
        if product.stock <= 0:
            continue

        qty = min(qty, product.stock)

        line_total = (product.price or Decimal("0.00")) * qty
        total += line_total
        items.append({"product": product, "qty": qty, "line_total": line_total})

    return items, total


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

    # Atomic: order creation + stock deduction
    with transaction.atomic():
        order = Order.objects.create(user=request.user, status=Order.STATUS_PENDING)

        for item in items:
            product = item["product"]
            qty = item["qty"]

            # Deduct stock safely (only if enough stock exists)
            updated = (
                Product.objects.filter(id=product.id, stock__gte=qty)
                .update(stock=F("stock") - qty)
            )
            if updated != 1:
                # If stock changed between page load and order placement
                raise Http404("Not enough stock to place this order. Please update your cart.")

            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                unit_price=product.price,
                quantity=qty,
            )

        # Clear session cart after successful order
        request.session["cart"] = {}
        request.session.modified = True

    return redirect("orders:detail", order_id=order.id)


@login_required
def order_detail(request, order_id: int):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})