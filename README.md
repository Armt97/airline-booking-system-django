# Airline Booking System (Django)

Django-based flight search and booking app with SQLite (dev), authentication, and clean UI. Ready for containerization and future PostgreSQL migration.

## Run Locally
```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install -r requirements.txt

# env
cp .env.example .env   # then edit values
python manage.py migrate
python manage.py runserver


## Environment Variables
Copy `.env.example` → `.env` and set at least:
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- DATABASE_URL (defaults to SQLite)

## Notes
- `.env` and `*.sqlite3` are ignored by Git.
- Add screenshots to `screenshots/` and link them here.
```
