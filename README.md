# Expense Tracker API (Django + DRF)

A Django REST Framework API for tracking expenses with user-based access control, categories, summary breakdowns, filtering, pagination, JWT auth, and seed data generation.

## Current Features

- Custom user model (`expensetracker.User`)
- Category management per user
- Expense CRUD with category mapping
- Per-user access isolation (staff can access all)
- Expense summary endpoint with category totals
- JWT token login/refresh
- Query filtering (user/category/amount/date)
- Pagination on expense list
- Management command to seed large sample datasets

## Tech Stack

- Python 3
- Django 6
- Django REST Framework
- djangorestframework-simplejwt
- django-filter
- SQLite (default)

## Project Structure

```text
.
├── api.http
├── README.md
└── core/
    ├── db.sqlite3
    ├── manage.py
    ├── core/
    │   ├── settings.py
    │   └── urls.py
    └── expensetracker/
        ├── models.py
        ├── serilizers.py
        ├── views.py
        ├── urls.py
        ├── filters.py
        └── management/
            └── commands/
                └── seed_expenses.py
```

## Setup

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Run migrations.
5. Create a superuser (optional but recommended).
6. Run the server.

```powershell
cd core
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django djangorestframework djangorestframework-simplejwt django-filter
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Authentication

JWT endpoints are available in the root URL config:

- `POST /api/token/` -> obtain access/refresh token
- `POST /api/token/refresh/` -> refresh access token

Example request:

```http
POST http://127.0.0.1:8000/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin"
}
```

Use the access token in headers:

```text
Authorization: Bearer <access_token>
```

## API Endpoints

Base routes from `expensetracker.urls`:

- `GET/POST /` -> list/create expenses
- `GET/POST /categories/` -> list/create categories
- `GET /summary/` -> total expense + category breakdown
- `GET/POST /create_category/`
- `GET/PUT/PATCH/DELETE /create_category/{id}/`
- `GET/POST /create_expense/`
- `GET/PUT/PATCH/DELETE /create_expense/{id}/`

## Filtering and Pagination

Expense list endpoint (`/`) supports:

- `user` (exact username, case-insensitive)
- `category` (contains)
- `min_amount`
- `max_amount`
- `start_date`
- `end_date`
- `page`
- `page_size` (max 100)

Example:

```text
GET /?category=bills&min_amount=100&max_amount=1000&start_date=2026-01-01&end_date=2026-12-31&page=1&page_size=20
```

## Seed Sample Data

A custom management command is included:

```powershell
cd core
python manage.py seed_expenses --username moiz --categories-per-user 5 --expenses-per-user 1000 --days-back 365
```

Options:

- `--username` (optional): seed only one user
- `--categories-per-user` (default: `5`)
- `--expenses-per-user` (default: `1200`)
- `--days-back` (default: `365`)

If `--username` is omitted, it seeds all users.

## Notes

- `Expense.id` is a UUID primary key.
- Category names are unique per user.
- Non-staff users only see their own records.

## License

No license file is currently defined in this repository.
