# Chingu Laundry

A small Django web app for a laundry shop: customers reserve a pickup and track their order with an **E-Faktur** number, staff see all orders on a dashboard. Built for Indonesian laundry businesses — the 10 service types (kiloan, cuci & setrika, dry cleaning, green dry cleaning, laundry sepatu, tas, karpet, gorden, kulit, lainnya) and WhatsApp contact reflect how a real local laundry shop works.

> Note: the "E-Faktur" here is a tracking code, not a bill — orders have no price, weight, or payment fields (yet).

## Features

- **Pickup reservation** (`/`) — customer fills in name, address, WhatsApp, laundry type, pickup date/time, and gets an auto-generated E-Faktur number (`EF` + 8 random letters/digits, e.g. `EF7K2P9QX4`). Server-side validation: WhatsApp must be 9–15 digits, pickup date can't be in the past.
- **Order tracking** (`/track/`) — enter an E-Faktur number to see the service, pickup slot, and status (pending → in progress → completed/cancelled). Address and WhatsApp are masked on this public page.
- **Staff dashboard** (`/dashboard/`) — table of all orders, newest first. Login + staff account required.
- **Django admin** (`/admin/`) — the place to change order status and manage orders.
- **Demo data** — `python manage.py seed_demo` creates 5 clearly-fake demo orders so the dashboard isn't empty on first run.

## Quickstart

Requires **Python 3.10+** (Django 5.2 needs it). No other system dependencies; the database is SQLite, the frontend is Tailwind via CDN (no build step).

```bash
git clone https://github.com/iambillgates/laundry-management-system.git
cd laundry-management-system

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env and set a real SECRET_KEY. Generate one with:
#   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# The app refuses to start without SECRET_KEY set.

python manage.py migrate

# Staff account for the dashboard (/dashboard/) and admin (/admin/):
python manage.py createsuperuser

# Optional demo orders (5 fake orders across statuses):
python manage.py seed_demo

python manage.py runserver
# Open http://127.0.0.1:8000/
```

## Configuration

All settings come from environment variables (see `.env.example`); nothing secret is hardcoded:

| Variable | Required | Default | Notes |
|---|---|---|---|
| `SECRET_KEY` | Yes | — | Long random string. The app won't start without it. |
| `DEBUG` | No | `False` | Set `True` only for local development. |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated hostnames the app may serve. |

## Project structure

```plaintext
laundry-management-system/
├── manage.py
├── requirements.txt            # Django==5.2.3 (the only dependency)
├── .env.example                # Copy to .env and fill in (never commit .env)
├── laundry_project/            # Django project settings + root URLs
│   ├── settings.py
│   ├── urls.py                 # /admin/ + includes laundry_app.urls
│   ├── wsgi.py
│   └── asgi.py
└── laundry_app/                # The laundry app
    ├── models.py               # LaundryOrder: E-Faktur, service types, status
    ├── views.py                # home, track_order (masked), dashboard (staff-only)
    ├── forms.py                # Reservation + tracking forms with validation
    ├── urls.py                 # / , /track/, /dashboard/
    ├── admin.py
    ├── templates/laundry_app/  # home.html, track_result.html, dashboard.html
    ├── migrations/
    └── management/commands/
        └── seed_demo.py        # Creates 5 demo orders (idempotent)
```

## License

MIT — see [LICENSE](LICENSE).
