# TaskFlow FastAPI Backend

## Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

The included `data/taskflow_product_health.db` is ready to use.

## Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Open http://127.0.0.1:8000/docs

## ElevenLabs tools
Use these endpoints as custom tools:
- POST /api/v1/product-metrics/query
- POST /api/v1/support/query
- POST /api/v1/support/monthly-trend
- POST /api/v1/customer-health/query
- POST /api/v1/feedback/query
- POST /api/v1/executive/overview

Do NOT expose arbitrary SQL to the voice agent.

## Local testing
ElevenLabs cloud cannot reach localhost. Use an HTTPS tunnel for development:
ngrok http 8000

Then use the HTTPS forwarding URL for the ElevenLabs tool/webhook.

## Security before production
Add API authentication, HTTPS, rate limiting, request IDs, audit logging, CORS restrictions and query timeouts. For larger concurrent workloads migrate from SQLite to PostgreSQL.
