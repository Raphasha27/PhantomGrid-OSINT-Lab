# PhantomGrid OSINT API — Documentation

> Autonomous Open Source Intelligence (OSINT) scraping and cyber threat aggregation engine.

## Base URL

```
http://localhost:8000
```

## Overview

PhantomGrid aggregates threat intelligence from multiple sources, providing:

- **Threat Scanning** — Scan domains for threat indicators
- **Intel Feed** — Browse collected intelligence sorted by severity
- **Actor Profiling** — Aggregate threat actor activity and attack vectors
- **Alert System** — High-severity alert feeds
- **IOC Feed** — Indicators of Compromise with MITRE ATT&CK TTPs

---

## Endpoints

### Health & Info

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Platform status and intel count |
| `GET` | `/health` | Health check |

### Scan

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/scan` | Initiate an OSINT scan |

### Intel

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/intel` | List intel entries (filterable by severity) |
| `GET` | `/api/v1/intel/{intel_id}` | Get a specific intel entry |

### Actors

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/actors` | List threat actors with aggregated stats |

### Alerts

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/alerts` | Get critical alerts (severity >= threshold) |

### IOC

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/ioc` | IOC feed with TTP mappings |

---

## Example Requests

### Scan a Domain

```bash
curl -X POST http://localhost:8000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{
    "target_domain": "darkforum-alpha.onion",
    "depth": 2,
    "keywords": ["breach", "exploit", "credential"]
  }'
```

**Response:**
```json
{
  "scan_id": "a1b2c3d4",
  "target": "darkforum-alpha.onion",
  "depth": 2,
  "keywords_matched": ["breach", "exploit", "credential"],
  "new_intel_entries": 5,
  "results": [...],
  "scan_duration_ms": 2340
}
```

### List Intel (High Severity)

```bash
curl "http://localhost:8000/api/v1/intel?limit=10&severity_min=7"
```

**Response:**
```json
{
  "total": 8,
  "entries": [
    {
      "id": "a1b2c3d4",
      "source_domain": "pastebin-mirror.net",
      "threat_actor": "APT-28",
      "attack_vector": "Phishing",
      "target_sector": "Financial Sector",
      "severity": 9,
      "confidence_score": 0.92,
      "ioc": "192.168.1.100",
      "ttps": "T1566",
      "discovered_at": "2025-01-14T08:20:00",
      "status": "ACTIVE"
    }
  ]
}
```

### Get Threat Actors

```bash
curl http://localhost:8000/api/v1/actors
```

### Get Critical Alerts

```bash
curl "http://localhost:8000/api/v1/alerts?severity_min=8"
```

### IOC Feed

```bash
curl http://localhost:8000/api/v1/ioc
```

**Response:**
```json
{
  "ioc_count": 15,
  "feed": [
    {
      "ioc": "192.168.1.100",
      "type": "IPv4",
      "severity": 8,
      "ttps": "T1566"
    }
  ]
}
```

---

## Intel Entry Schema

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `source_domain` | string | Source domain where intel was found |
| `threat_actor` | string | Attribution (e.g., APT-28, Lazarus Group) |
| `attack_vector` | string | Attack type (e.g., Phishing, Ransomware) |
| `target_sector` | string | Target industry sector |
| `severity` | int (1-10) | Threat severity level |
| `confidence_score` | float (0-1) | Confidence in the intel |
| `ioc` | string | Indicator of Compromise (IP, hash, etc.) |
| `ttps` | string | MITRE ATT&CK technique ID |
| `status` | string | ACTIVE, MONITORING, CONTAINED, ESCALATED |

---

## Interactive Docs

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec:** [`docs/api-spec.yaml`](./api-spec.yaml)
