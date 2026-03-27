def cart_item_count(request):
    cart = request.session.get("cart", {})
    count = 0
    for item in cart.values():
        try:
            count += int(item.get("qty", 0))
        except (TypeError, ValueError):
            pass
    return {"cart_item_count": count}