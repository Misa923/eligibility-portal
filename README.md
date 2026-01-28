# Eligibility Portal (Django)

Partner portal where:

- Partners create accounts and submit eligibility-check requests via HTML templates.
- Each request contains **any number** of client rows (First, Middle, Last + DOB).
- Staff/admin reviews each request and marks each client **Eligible / Not eligible** and can add notes.
- Emails are sent:
  - To admin when a request is submitted
  - To partner when staff responds
- **Retention:** active requests are archived + deleted after 30 days, but an audit record is kept (who requested, when, and the eligibility results, plus name/DOB).

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Partner portal: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Staff review queue: http://127.0.0.1:8000/review/  (staff only)

## Database: SQLite (dev) or Postgres (prod)

This project uses `DATABASE_URL` when set (Postgres recommended for production). If not set, it falls back to SQLite for local development.

Example Postgres connection string:

```
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DBNAME
```

## Email

By default, emails print to the console. For real email, set `EMAIL_BACKEND` and SMTP variables.

Required env vars:
- `ADMIN_NOTIFY_EMAIL`
- `DEFAULT_FROM_EMAIL`

## Retention / archiving (30 days)

Run:

```bash
python manage.py archive_expired_requests
```

Options:
- `--days 30` (default)
- `--dry-run`

In production, run this daily using your host's scheduled job / cron.
