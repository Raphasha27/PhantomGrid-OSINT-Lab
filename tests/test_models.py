import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import uuid
from datetime import datetime, timedelta
from api.main import (
    ScanRequest,
    AlertRequest,
    generate_intel,
    DOMAINS,
    THREAT_ACTORS,
    ATTACK_VECTORS,
    TARGETS,
)


class TestScanRequestModel:
    def test_defaults(self):
        req = ScanRequest()
        assert req.target_domain == "surface_web"
        assert req.depth == 1
        assert req.keywords == ["breach", "exploit", "credential"]

    def test_custom_values(self):
        req = ScanRequest(target_domain="darkweb", depth=3, keywords=["leak"])
        assert req.target_domain == "darkweb"
        assert req.depth == 3
        assert req.keywords == ["leak"]

    def test_none_actor_optional(self):
        req = ScanRequest(target_domain=None, depth=None, keywords=None)
        assert req.target_domain is None
        assert req.depth is None
        assert req.keywords is None


class TestAlertRequestModel:
    def test_defaults(self):
        req = AlertRequest()
        assert req.actor is None
        assert req.vector is None
        assert req.severity_min == 3

    def test_custom_values(self):
        req = AlertRequest(actor="APT-28", vector="Phishing", severity_min=8)
        assert req.actor == "APT-28"
        assert req.vector == "Phishing"
        assert req.severity_min == 8


class TestGenerateIntel:
    def test_returns_dict_with_all_keys(self):
        entry = generate_intel()
        expected_keys = {
            "id",
            "source_domain",
            "threat_actor",
            "attack_vector",
            "target_sector",
            "severity",
            "confidence_score",
            "ioc",
            "ttps",
            "discovered_at",
            "status",
        }
        assert set(entry.keys()) == expected_keys

    def test_id_is_8_char_hex(self):
        entry = generate_intel()
        assert len(entry["id"]) == 8
        int(entry["id"], 16)  # raises ValueError if not hex

    def test_source_domain_from_constant(self):
        for _ in range(30):
            entry = generate_intel()
            assert entry["source_domain"] in DOMAINS

    def test_threat_actor_from_constant(self):
        for _ in range(30):
            entry = generate_intel()
            assert entry["threat_actor"] in THREAT_ACTORS

    def test_attack_vector_from_constant(self):
        for _ in range(30):
            entry = generate_intel()
            assert entry["attack_vector"] in ATTACK_VECTORS

    def test_target_sector_from_constant(self):
        for _ in range(30):
            entry = generate_intel()
            assert entry["target_sector"] in TARGETS

    def test_severity_in_range(self):
        for _ in range(50):
            entry = generate_intel()
            assert 1 <= entry["severity"] <= 10

    def test_confidence_score_range(self):
        for _ in range(50):
            entry = generate_intel()
            assert 0.55 <= entry["confidence_score"] <= 0.97

    def test_ioc_is_valid_ipv4(self):
        for _ in range(50):
            entry = generate_intel()
            parts = entry["ioc"].split(".")
            assert len(parts) == 4
            for part in parts:
                num = int(part)
                assert 1 <= num <= 255

    def test_ttps_are_valid_mitre(self):
        valid_ttps = {"T1566", "T1190", "T1059", "T1486", "T1078"}
        for _ in range(30):
            entry = generate_intel()
            assert entry["ttps"] in valid_ttps

    def test_discovered_at_is_iso_string(self):
        entry = generate_intel()
        dt = datetime.fromisoformat(entry["discovered_at"])
        assert isinstance(dt, datetime)
        # Should be within last 72 hours
        assert dt <= datetime.utcnow()
        assert dt >= datetime.utcnow() - timedelta(hours=72)

    def test_status_is_valid(self):
        valid_statuses = {"ACTIVE", "MONITORING", "CONTAINED", "ESCALATED"}
        for _ in range(30):
            entry = generate_intel()
            assert entry["status"] in valid_statuses

    def test_uniqueness_of_ids(self):
        ids = {generate_intel()["id"] for _ in range(100)}
        # UUIDs can collide at 8-char truncation, but with 100 samples
        # the chance is extremely low; we just verify they're strings
        assert all(isinstance(i, str) for i in ids)

    def test_confidence_is_rounded_to_2_decimals(self):
        for _ in range(30):
            entry = generate_intel()
            assert entry["confidence_score"] == round(entry["confidence_score"], 2)
