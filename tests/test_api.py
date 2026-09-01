import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ONLINE"
    assert data["platform"] == "PhantomGrid-OSINT"


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_scan():
    resp = client.post(
        "/api/v1/scan",
        json={"target_domain": "test", "depth": 1, "keywords": ["breach"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "scan_id" in data
    assert "results" in data
    assert data["new_intel_entries"] > 0


def test_list_intel():
    resp = client.get("/api/v1/intel?limit=5&severity_min=1")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "entries" in data


def test_get_intel_not_found():
    resp = client.get("/api/v1/intel/nonexistent")
    assert resp.status_code == 404


def test_list_actors():
    resp = client.get("/api/v1/actors")
    assert resp.status_code == 200
    data = resp.json()
    assert "threat_actors" in data


def test_alerts():
    resp = client.get("/api/v1/alerts?severity_min=7")
    assert resp.status_code == 200
    data = resp.json()
    assert "critical_alerts" in data
    assert "alerts" in data


def test_ioc_feed():
    resp = client.get("/api/v1/ioc")
    assert resp.status_code == 200
    data = resp.json()
    assert "ioc_count" in data
    assert "feed" in data
