import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from api.main import (
    ATTACK_VECTORS,
    DOMAINS,
    THREAT_ACTORS,
    app,
    generate_intel,
    intel_store,
)
from fastapi.testclient import TestClient

client = TestClient(app)


class TestIntelStoreSeed:
    def test_store_has_initial_entries(self):
        assert len(intel_store) >= 15

    def test_seed_entries_are_valid(self):
        for entry in intel_store:
            assert "id" in entry
            assert "severity" in entry
            assert 1 <= entry["severity"] <= 10
            assert entry["source_domain"] in DOMAINS
            assert entry["threat_actor"] in THREAT_ACTORS


class TestScanEndpoint:
    def test_scan_adds_entries_to_store(self):
        before = len(intel_store)
        resp = client.post(
            "/api/v1/scan",
            json={
                "target_domain": "test.io",
                "depth": 2,
                "keywords": ["malware"],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["new_intel_entries"] >= 2
        assert len(intel_store) > before

    def test_scan_returns_correct_target(self):
        resp = client.post("/api/v1/scan", json={"target_domain": "evil.onion"})
        assert resp.json()["target"] == "evil.onion"

    def test_scan_returns_scan_duration(self):
        resp = client.post("/api/v1/scan", json={})
        assert "scan_duration_ms" in resp.json()
        assert isinstance(resp.json()["scan_duration_ms"], int)

    def test_scan_results_match_count(self):
        resp = client.post("/api/v1/scan", json={})
        data = resp.json()
        assert len(data["results"]) == data["new_intel_entries"]

    def test_scan_result_has_required_fields(self):
        resp = client.post("/api/v1/scan", json={})
        for entry in resp.json()["results"]:
            assert "id" in entry
            assert "threat_actor" in entry
            assert "severity" in entry
            assert "ioc" in entry


class TestListIntel:
    def test_list_intel_respects_limit(self):
        resp = client.get("/api/v1/intel?limit=3")
        assert len(resp.json()["entries"]) <= 3

    def test_list_intel_filters_by_severity(self):
        resp = client.get("/api/v1/intel?severity_min=8")
        for entry in resp.json()["entries"]:
            assert entry["severity"] >= 8

    def test_list_intel_sorted_descending(self):
        resp = client.get("/api/v1/intel")
        severities = [e["severity"] for e in resp.json()["entries"]]
        assert severities == sorted(severities, reverse=True)

    def test_list_intel_total_matches_filter(self):
        resp = client.get("/api/v1/intel?severity_min=5")
        total = resp.json()["total"]
        assert total >= 0
        assert len(resp.json()["entries"]) <= total

    def test_list_intel_empty_when_severity_too_high(self):
        resp = client.get("/api/v1/intel?severity_min=100")
        assert resp.json()["total"] == 0
        assert resp.json()["entries"] == []


class TestGetIntelById:
    def test_get_existing_intel(self):
        entry = intel_store[0]
        resp = client.get(f"/api/v1/intel/{entry['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == entry["id"]

    def test_get_intel_not_found(self):
        resp = client.get("/api/v1/intel/zzzzzzzz")
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()


class TestListActors:
    def test_actors_returns_list(self):
        resp = client.get("/api/v1/actors")
        assert resp.status_code == 200
        assert isinstance(resp.json()["threat_actors"], list)

    def test_actor_entry_structure(self):
        resp = client.get("/api/v1/actors")
        for actor in resp.json()["threat_actors"]:
            assert "actor" in actor
            assert "count" in actor
            assert "avg_severity" in actor
            assert "vectors" in actor
            assert actor["count"] >= 1
            assert isinstance(actor["vectors"], list)

    def test_actor_avg_severity_is_valid(self):
        resp = client.get("/api/v1/actors")
        for actor in resp.json()["threat_actors"]:
            assert 1 <= actor["avg_severity"] <= 10

    def test_actor_vectors_are_valid(self):
        resp = client.get("/api/v1/actors")
        for actor in resp.json()["threat_actors"]:
            for v in actor["vectors"]:
                assert v in ATTACK_VECTORS


class TestAlerts:
    def test_alerts_filters_by_severity(self):
        resp = client.get("/api/v1/alerts?severity_min=9")
        for alert in resp.json()["alerts"]:
            assert alert["severity"] >= 9

    def test_alerts_sorted_descending(self):
        resp = client.get("/api/v1/alerts?severity_min=1")
        severities = [a["severity"] for a in resp.json()["alerts"]]
        assert severities == sorted(severities, reverse=True)

    def test_alerts_count_matches_list(self):
        resp = client.get("/api/v1/alerts?severity_min=7")
        data = resp.json()
        assert data["critical_alerts"] == len(data["alerts"])

    def test_alerts_empty_when_threshold_impossible(self):
        resp = client.get("/api/v1/alerts?severity_min=100")
        assert resp.json()["critical_alerts"] == 0
        assert resp.json()["alerts"] == []


class TestIOCFeed:
    def test_ioc_feed_structure(self):
        resp = client.get("/api/v1/ioc")
        data = resp.json()
        assert "ioc_count" in data
        assert "feed" in data
        assert data["ioc_count"] == len(data["feed"])

    def test_ioc_entry_fields(self):
        resp = client.get("/api/v1/ioc")
        for ioc in resp.json()["feed"]:
            assert "ioc" in ioc
            assert ioc["type"] == "IPv4"
            assert "severity" in ioc
            assert "ttps" in ioc

    def test_ioc_count_matches_store(self):
        resp = client.get("/api/v1/ioc")
        assert resp.json()["ioc_count"] == len(intel_store)


class TestRootAndHealth:
    def test_root_intel_entries_match_store(self):
        resp = client.get("/")
        assert resp.json()["intel_entries"] == len(intel_store)

    def test_health_returns_iso_timestamp(self):
        resp = client.get("/health")
        ts = resp.json()["timestamp"]
        from datetime import datetime

        dt = datetime.fromisoformat(ts)
        assert isinstance(dt, datetime)


class TestGenerateIntelUnit:
    def test_generate_intel_returns_dict(self):
        entry = generate_intel()
        assert isinstance(entry, dict)

    def test_generate_intel_multiple_unique_sources(self):
        entries = [generate_intel() for _ in range(20)]
        sources = {e["source_domain"] for e in entries}
        # With 5 domains and 20 samples, likely to see multiple
        assert len(sources) >= 2

    def test_generate_intel_multiple_statuses(self):
        entries = [generate_intel() for _ in range(50)]
        statuses = {e["status"] for e in entries}
        assert len(statuses) >= 2
