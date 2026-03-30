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
        messages.info(request, "Your cart is empty.")
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
                # Stock changed between checkout page load and placing the order
                messages.error(
                    request,
                    f"Sorry, '{product.name}' doesn't have enough stock to fulfill your order. "
                    "Please review your cart and try again."
                )
                # Rollback transaction
                raise transaction.TransactionManagementError("Insufficient stock during checkout.")

            OrderItem.objects.create(
                order=order,
                product_name=product.name,
                unit_price=product.price,
                quantity=qty,
            )

        # Clear cart after successful order
        request.session["cart"] = {}
        request.session.modified = True

    messages.success(request, f"Order #{order.id} placed successfully.")
    return redirect("orders:detail", order_id=order.id)
