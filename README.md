# PagePress Books — Single Vendor E-commerce Website (Django)

A simple single-vendor e-commerce website for a **Book Shop**, built with Django, Bootstrap 5,
vanilla JavaScript, and custom CSS.

## Features

- **Home page** — shop name/logo, navbar, Bootstrap hero banner, product categories, featured
  products, footer.
- **Product listing page** — products loaded from the database, with search and category filter.
- **Product detail page** — image, name, price, description, available quantity, Add to Cart.
- **Shopping cart** (session-based) — add, increase, decrease, remove, edit quantity directly,
  live total price recalculation in JavaScript.
- **Checkout page** — Bootstrap form (name, phone, address) with client-side validation; saves
  the customer and order to the database and reduces stock; shows "Order Placed Successfully!".
- **Django Admin** — full product/category/customer/order management.

## Models

- `Category` — name, slug
- `Product` — name, category, price, description, image, quantity, is_featured
- `Customer` — name, phone, address
- `Order` — customer, product, quantity, total_price, order_date (plus `order_group`, used to
  group the multiple order lines created from one checkout submission)

## Project Structure

```
ecommerce_project/
├── manage.py
├── requirements.txt
├── ecommerce/            # Project settings, root urls
└── shop/                 # Main app
    ├── models.py         # Category, Product, Customer, Order
    ├── views.py          # Home, product list/detail, cart, checkout, order success
    ├── urls.py
    ├── forms.py          # CheckoutForm
    ├── cart.py           # Session-based cart helper class
    ├── admin.py
    ├── management/commands/seed_data.py   # optional sample-data loader
    ├── templates/shop/   # base.html, home.html, products.html, product_detail.html,
    │                     # cart.html, checkout.html, order_success.html
    └── static/shop/      # style.css, script.js
```

## Setup Instructions

1. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **(Optional) Load sample books** so the shop isn't empty on first run:
   ```bash
   python manage.py seed_data
   ```

5. **Create an admin account**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the shop and `http://127.0.0.1:8000/admin/` to manage
   products, categories, customers, and orders.

7. **Add real products with images** through the Admin Panel: log in at `/admin/`, open
   **Products**, and add at least 5 books with an uploaded image, price, description, and
   quantity. Uploaded images are stored under `media/products/`.

## How Each Requirement Is Met

| Requirement | Where |
|---|---|
| URL Routing | `ecommerce/urls.py`, `shop/urls.py` |
| Views | `shop/views.py` (function-based views) |
| Models | `shop/models.py` |
| Database | SQLite via Django ORM (default `settings.py`) |
| Templates | `shop/templates/shop/*.html`, extending `base.html` |
| Forms | `shop/forms.py` (`CheckoutForm`, a `ModelForm` for `Customer`) |
| Admin Panel | `shop/admin.py` — all 4 models registered with list/search/filter config |
| JavaScript | `shop/static/shop/js/script.js` — live cart total recalculation, checkout form validation, auto-dismissing alerts |
| Bootstrap | Navbar, banner, cards, buttons, grid, alerts, forms across all templates |

## Bonus Features Included

- **Product search** (`/products/?q=...`) — searches product name and description.
- **Category filter** (`/products/?category=<slug>`) — sidebar filter on the products page.
- Stock is automatically reduced when an order is placed, and "Add to Cart" is disabled once a
  product is out of stock.

## Notes

- The cart is stored in the Django **session** (not the database), so it's tied to the visitor's
  browser and clears itself after checkout.
- Because the `Order` model stores one product per row, placing an order with multiple different
  items in the cart creates one `Order` row per product, all sharing the same `order_group` value
  and `order_date`, so they can still be displayed and totalled together.
