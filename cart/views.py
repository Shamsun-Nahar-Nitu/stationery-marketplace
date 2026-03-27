from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product


def _get_cart(session):
    """
    Cart stored in session as:
    {
      "<product_id>": {"qty": 2},
      ...
    }
    """
    cart = session.get("cart")
    if cart is None:
        cart = session["cart"] = {}
    return cart


@require_POST
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = _get_cart(request.session)

    pid = str(product.id)
    if pid not in cart:
        cart[pid] = {"qty": 0}

    cart[pid]["qty"] += 1
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
    cart = _get_cart(request.session)
    pid = str(product_id)

    try:
        qty = int(request.POST.get("qty", 1))
    except ValueError:
        qty = 1

    if qty <= 0:
        cart.pop(pid, None)
    else:
        # Optional: cap quantity to something reasonable
        qty = min(qty, 999)
        cart[pid] = {"qty": qty}

    request.session.modified = True
    return redirect("cart:detail")


def cart_detail(request):
    cart = _get_cart(request.session)

    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    # Build a view model for template
    items = []
    total = Decimal("0.00")

    # Map for quick lookup
    product_map = {p.id: p for p in products}

    for pid_str, data in cart.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if not product:
            continue

        qty = int(data.get("qty", 0))
        line_total = (product.price or Decimal("0.00")) * qty
        total += line_total

        items.append(
            {
                "product": product,
                "qty": qty,
                "line_total": line_total,
            }
        )

    return render(request, "cart/detail.html", {"items": items, "total": total})