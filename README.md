# Stationery Marketplace (Multi‑Vendor) — Django + PostgreSQL

A multi-vendor stationery marketplace built with **Django** and **PostgreSQL**.  
This project is being built step-by-step and is currently under active development.

## Status
**Under construction** (active development)

---

## Features implemented so far

### Vendor + Catalog
- `vendors` app: `SellerProfile`
- `catalog` app:
  - `Category`
  - `Product` (belongs to a seller and optional category)
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

## Main URLs
- `/` — Product list
- `/p/<slug>/` — Product detail
- `/cart/` — Cart detail
- `/admin/` — Admin

---

## Tech stack
- Python / Django
- PostgreSQL
- HTML templates (Django templates)
- Session-based cart

---

## Local development

### 1) Clone the repository
```bash
git clone https://github.com/Shamsun-Nahar-Nitu/stationery-marketplace.git
cd stationery-marketplace
```

### 2) Create and activate a virtual environment
```bash
python -m venv .venv
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Configure environment variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=stationery
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
```

> Note: Variable names should match what your Django `settings.py` expects.  
> If you change the names, update `settings.py` accordingly.

### 5) Start PostgreSQL
If you’re using Docker for Postgres, start your container (or `docker compose up -d` if you have a compose file).

### 6) Run migrations and start the server
```bash
python manage.py migrate
python manage.py runserver
```

Open:
- http://127.0.0.1:8000/ (product list)
- http://127.0.0.1:8000/cart/ (cart)
- http://127.0.0.1:8000/admin/ (admin)

---

## Demo data (via Admin)

1. Create a Django superuser:
```bash
python manage.py createsuperuser
```

2. In `/admin/`, create:
   1) a User (seller)  
   2) a `SellerProfile` for that user  
   3) a `Category`  
   4) a `Product` with a positive `stock`

Then visit `/` and add the product to the cart.

---

## Project structure (high level)
- `vendors/` — vendor/seller related models and logic
- `catalog/` — categories + products
- `cart/` (or similar) — session-based cart behavior

---

---


