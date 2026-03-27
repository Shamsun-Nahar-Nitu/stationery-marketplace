# Stationery Marketplace — Under Construction

**Status:** Under construction (active development)

A multi-vendor stationery marketplace built with Django and PostgreSQL.

---

## What’s implemented so far

### Vendor + Catalog
- `vendors` app: `SellerProfile`
- `catalog` app: `Category`, `Product` (product belongs to a seller and optional category)
- Admin support for managing sellers, categories, and products
- Public pages:
  - Product list (homepage)
  - Product detail

### Cart (session-based)
- Add to cart
- Update quantity
- Remove from cart
- Cart detail page with totals
- Stock rules:
  - Can’t add more than available stock
  - Updating quantity clamps to available stock
  - “Out of stock” disables add-to-cart
  - “Only X left” message when stock is low

---

## Apps / main URLs

- `/` — Product list
- `/p/<slug>/` — Product detail
- `/cart/` — Cart detail
- `/admin/` — Admin

---

## Local development (quick)

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure environment
Create a `.env` file in the project root and set:
- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`

### 3) Start PostgreSQL (Docker)
Start your PostgreSQL container (project uses Docker for Postgres).

### 4) Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

---

## Demo data (via Admin)

Create:
1. a User (seller)
2. a `SellerProfile` for that user
3. a `Category`
4. a `Product` with a positive `stock`

Then visit `/` and add the product to the cart.

---



---
