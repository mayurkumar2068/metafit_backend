# MetaFit Backend (Django API)

Backend scaffold created outside Flutter project at:
`/Users/mayurbobade/Documents/metafit_backend`

## Implemented now

- Django + DRF project initialized
- Custom user model (`mobile_number`, `email`, `full_name`)
- Auth APIs:
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/refresh`
- JWT access + refresh token response
- Refresh token rotation/blacklist enabled
- Basic API test added

## Login API contract

Request body:

```json
{
  "mobile_number": "9876543210",
  "email": "mayur@example.com",
  "full_name": "Mayur Bobade"
}
```

Behavior:
- If mobile does not exist -> user created
- If mobile exists -> name/email updated (if changed)
- Returns access/refresh JWT tokens

## Setup

```bash
cd "/Users/mayurbobade/Documents/metafit_backend"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database

Default:
- SQLite for quick local run

MySQL mode:
- create `.env` from `.env.example`:

```bash
cp .env.example .env
```

- update `.env` values with your MySQL credentials (`DB_ENGINE=mysql`)
- if you see `RuntimeError: 'cryptography' package is required...`, run:

```bash
pip install -r requirements.txt
```

## Migrate and run

```bash
cd "/Users/mayurbobade/Documents/metafit_backend"
source .venv/bin/activate
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Quick test (curl)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "mobile_number":"9876543210",
    "email":"mayur@example.com",
    "full_name":"Mayur Bobade"
  }'
```

## API Docs (Swagger)

- Swagger UI: `http://127.0.0.1:8000/swagger/`
- ReDoc: `http://127.0.0.1:8000/redoc/`
- OpenAPI JSON: `http://127.0.0.1:8000/swagger.json`

## Next APIs to add

- onboarding (`/api/v1/onboarding/*`)
- home dashboard aggregate (`/api/v1/dashboard/home`)
- daily check-ins (`/api/v1/checkins/*`)
- progress/insights (`/api/v1/progress/*`, `/api/v1/insights/*`)
- protocol + side-effects (`/api/v1/protocols/*`, `/api/v1/side-effects/*`)
- export jobs (`/api/v1/exports/*`)
