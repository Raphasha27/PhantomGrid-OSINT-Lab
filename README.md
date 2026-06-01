# PhantomGrid-OSINT-Lab

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?logo=fastapi&logoColor=white&style=for-the-badge)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white&style=for-the-badge)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![Branch](https://img.shields.io/badge/Branch-experimental%2Fv1-00bfff?style=for-the-badge)](#)
[![Safety](https://img.shields.io/badge/Protocol-Isolated%20Lab-8957e5?style=for-the-badge)](#)

Autonomous cyber intelligence and OSINT threat aggregation engine. PhantomGrid-OSINT-Lab is a FastAPI-based API that simulates Open Source Intelligence (OSINT) scraping, threat actor tracking, IoC (Indicators of Compromise) generation, and real-time cyber alerting — all with synthetic data in an isolated lab environment.

---

## Overview

PhantomGrid-OSINT-Lab models the workflows of a cyber threat intelligence platform, providing endpoints for domain scanning, threat actor profiling, alert management, and IoC feed generation. The system operates entirely on synthetic data, making it safe for development, demonstration, and educational use.

## Features

- **Automated Threat Scanning** — Simulate OSINT scans against target domains with configurable depth and keyword matching
- **Threat Actor Intelligence** — Profile and track threat actors (APT-28, Lazarus Group, etc.) with severity and attack vector analysis
- **Critical Alerting** — Real-time critical alert feed for high-severity threats (severity >= 7)
- **IOC Feed** — Generate and export synthetic Indicators of Compromise (IPs, TTPs) in a standardized feed format
- **Intel Repository** — In-memory intel store with search, filter, and severity-based sorting
- **CORS Enabled** — Ready for frontend dashboard integration

## Quick Start

```bash
git clone https://github.com/Raphasha27/PhantomGrid-OSINT-Lab.git
cd PhantomGrid-OSINT-Lab
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

Or with Docker:

```bash
docker build -t phantomgrid-osint .
docker run -p 8000:8000 phantomgrid-osint
```

## API Endpoints

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status and intel count |
| GET | `/health` | Health check |

### Intelligence Operations

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/scan` | Execute an OSINT scan |
| GET | `/api/v1/intel` | List intel entries (filtered by severity) |
| GET | `/api/v1/intel/{intel_id}` | Get specific intel entry |
| GET | `/api/v1/actors` | Threat actor profiling and statistics |
| GET | `/api/v1/alerts` | Critical alerts (severity >= 7) |
| GET | `/api/v1/ioc` | Indicators of Compromise feed |

### Scan Request

```json
{
  "target_domain": "surface_web",
  "depth": 1,
  "keywords": ["breach", "exploit", "credential"]
}
```

### Scan Response

```json
{
  "scan_id": "a1b2c3d4",
  "target": "surface_web",
  "new_intel_entries": 5,
  "scan_duration_ms": 2340,
  "results": [
    {
      "id": "e5f6g7h8",
      "source_domain": "darkforum-alpha.onion",
      "threat_actor": "APT-28",
      "attack_vector": "Phishing",
      "severity": 8,
      "ioc": "192.168.1.100",
      "ttps": "T1566"
    }
  ]
}
```

## Project Structure

```
PhantomGrid-OSINT-Lab/
├── api/
│   └── main.py           # FastAPI application with OSINT engine
├── tests/                # Unit tests
├── Dockerfile            # Container build
├── .dockerignore         # Docker build exclusions
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata and build config
└── .pre-commit-config.yaml
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check api/
ruff format api/ --check
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

**Safety Protocol**: This repository is an isolated lab environment. No production database connections, no live DNS routing, and no real threat data. Default branch: `experimental/v1`.

---

© 2026 **Kirov Dynamics Technology** | Built by **Koketso Raphasha (Raphasha27)**
