from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    assert client.get("/health").status_code==200

def test_company():
    r=client.get("/api/v1/company/overview")
    assert r.status_code==200
    assert r.json()["data"]["paying_customers"]==9764

def test_conversion():
    r=client.post("/api/v1/product-metrics/query",json={
        "metric":"free_to_paid_conversion_pct","start_month":"2026-07-01","end_month":"2026-08-01"})
    assert r.status_code==200
    assert r.json()["results"][-1]["value"]==8.4

def test_support_growth():
    r=client.post("/api/v1/support/monthly-trend")
    rows=r.json()["results"]
    aug=[x for x in rows if x["month"]=="2026-08"][0]
    assert aug["ticket_count"]==500
    assert aug["mom_change_pct"]==25.0
