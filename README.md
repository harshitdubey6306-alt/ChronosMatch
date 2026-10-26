# ChronosMatch API (FastAPI + PostgreSQL)

## Run
    cp .env.example .env
    docker compose up --build          # Postgres + API on :8000
    # or locally: pip install -r requirements.txt && uvicorn app.main:app --reload

Docs: http://localhost:8000/docs

## Try it
    curl -X POST localhost:8000/api/v1/auth/register -H 'content-type: application/json' \
         -d '{"email":"a@b.com","password":"password123"}'
    curl -X POST localhost:8000/api/v1/auth/login -d 'username=a@b.com&password=password123'
    # websocket: ws://localhost:8000/api/v1/ws/trades?token=<JWT>
    # then POST /api/v1/orders/ and watch the "orders" stream update live.

Make a user admin (needed for POST /trades):
    docker compose exec db psql -U chronos chronosmatch -c "UPDATE users SET role='admin' WHERE email='a@b.com';"

## Production notes
- Replace create_all with Alembic: `alembic init -t async alembic`, point env.py at app.db.base.Base.
- Run multiple workers: `uvicorn app.main:app --workers 4` (LISTEN/NOTIFY keeps websockets in sync).
- Set a real SECRET_KEY and restrict CORS origins.
