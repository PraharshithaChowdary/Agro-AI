import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "AGRO AI" in data["app"]
    assert len(data["features"]) == 3

def test_production_health():
    response = client.get("/api/production/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "crop_disease" in data["supported_analyses"]
