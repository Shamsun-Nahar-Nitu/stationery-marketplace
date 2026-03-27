from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product


def _get_cart(session):
    cart = session.get("cart")
    if cart is None:
        cart = session["cart"] = {}
    return cart


@require_POST
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)

    pid = str(product.id)
    current_qty = int(cart.get(pid, {}).get("qty", 0))

    # Respect stock:
    # - If stock is 0 => don't add
    # - Don't allow qty to exceed stock
    if product.stock <= 0:
        return redirect("cart:detail")

    new_qty = min(current_qty + 1, product.stock)
    cart[pid] = {"qty": new_qty}

    request.session.modified = True
    return redirect("cart:detail")


@require_POST
def cart_remove(request, product_id: int):
    cart = _get_cart(request.session)
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
        request.session.modified = True
    return redirect("cart:detail")


@require_POST
def cart_update(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)
    pid = str(product_id)

    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = 1

    # qty <= 0 removes
    if qty <= 0:
        cart.pop(pid, None)
        request.session.modified = True
        return redirect("cart:detail")

    # Respect stock
    if product.stock <= 0:
        cart.pop(pid, None)
        request.session.modified = True
        return redirect("cart:detail")

    qty = min(qty, product.stock)
    cart[pid] = {"qty": qty}

    request.session.modified = True
    return redirect("cart:detail")


def cart_detail(request):
    cart = _get_cart(request.session)

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    items = []
    total = Decimal("0.00")

    product_map = {p.id: p for p in products}

    # Optional cleanup: if stock became 0, remove from cart
    changed = False

    for pid_str, data in list(cart.items()):
        pid = int(pid_str)
        product = product_map.get(pid)

        if not product:
            continue

        qty = int(data.get("qty", 0))

        # Respect stock when stock changes after item is already in cart
        if product.stock <= 0:
            cart.pop(pid_str, None)
            changed = True
            continue

        if qty > product.stock:
            qty = product.stock
            cart[pid_str] = {"qty": qty}
            changed = True

        line_total = (product.price or Decimal("0.00")) * qty
        total += line_total

        items.append({"product": product, "qty": qty, "line_total": line_total})

    if changed:
        request.session.modified = True

    return render(request, "cart/detail.html", {"items": items, "total": total})