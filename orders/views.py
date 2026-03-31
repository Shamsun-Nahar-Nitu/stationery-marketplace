from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from .models import Order, OrderItem


def _get_cart(session):
    cart = session.get("cart")
    if cart is None:
        cart = session["cart"] = {}
    return cart


def _build_cart_items(cart):
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
    return render(request, "orders/checkout.html", {"items": items, "total": total})


@login_required
@require_POST
def place_order(request):
    cart = _get_cart(request.session)
    items, cart_total = _build_cart_items(cart)

    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    try:
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                status=Order.STATUS_PENDING,
                subtotal=Decimal("0.00"),
                total=Decimal("0.00"),
            )

            subtotal = Decimal("0.00")

            for item in items:
                product = Product.objects.select_for_update().get(id=item["product"].id)
                qty = item["qty"]

                if product.stock < qty:
                    messages.error(
                        request,
                        f"Sorry, '{product.name}' has only {product.stock} left. "
                        "Please update your cart and try again."
                    )
                    raise ValueError("Insufficient stock")

                unit_price = product.price or Decimal("0.00")
                line_total = unit_price * qty
                subtotal += line_total

                product.stock = product.stock - qty
                product.save(update_fields=["stock"])

                OrderItem.objects.create(
                    order=order,
                    product_name=product.name,
                    unit_price=unit_price,
                    quantity=qty,
                )

            # For now: total == subtotal (no shipping/tax yet)
            order.subtotal = subtotal
            order.total = subtotal
            order.save(update_fields=["subtotal", "total"])

            request.session["cart"] = {}
            request.session.modified = True

    except (ValueError, Product.DoesNotExist, DatabaseError):
        return redirect("cart:detail")

    messages.success(request, f"Order #{order.id} placed successfully.")
    return redirect("orders:detail", order_id=order.id)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})


@login_required
def order_detail(request, order_id: int):
    order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id, user=request.user)
    return render(request, "orders/order_detail.html", {"order": order})