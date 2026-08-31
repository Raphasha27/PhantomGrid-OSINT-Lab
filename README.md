[![CI](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# PhantomGrid OSINT Lab

### Open Source Intelligence Reconnaissance & IoC Tracking Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)

</div>

---

## Overview

PhantomGrid OSINT Lab is an **autonomous cyber intelligence and threat aggregation engine** built with FastAPI. It simulates Open Source Intelligence (OSINT) scraping, threat actor tracking, IoC (Indicators of Compromise) generation, and real-time cyber alerting — all with synthetic data in an isolated lab environment.

> **Safety Protocol**: Isolated lab environment. No production database connections, no live DNS routing, no real threat data.

---

## Features

- [x] IoC Extraction — Automated Indicators of Compromise generation (IPs, TTPs, domains)
- [x] Domain/IP Correlation — Cross-reference IOCs across multiple source domains
- [x] Threat Actor Profiling — Track APT groups with severity and attack vector analysis
- [x] Dark Web Monitoring Stub — Simulated .onion source aggregation
- [x] Feed Aggregation — Standardised IoC feed export for SIEM integration
- [x] Real-time Alerting — Critical alert feed for high-severity threats (severity >= 7)
- [x] API-First Design — Full REST API with OpenAPI documentation
- [x] CORS Enabled — Ready for frontend dashboard integration

---

## Architecture

```
┌─────────────────┐
│  Dashboard UI   │
│  (Static/SPA)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   :8000         │
│  ┌────────────┐ │
│  │ OSINT      │ │
│  │ Engine     │ │
│  └─────┬──────┘ │
└────────┼────────┘
         │
    ┌────▼────────────┐
    │  In-Memory Store │
    │  (Synthetic Data)│
    └─────────────────┘
```

---

## Quick Start

### Using pip + uvicorn

```bash
git clone https://github.com/Raphasha27/PhantomGrid-OSINT-Lab.git
cd PhantomGrid-OSINT-Lab
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### Using Docker

```bash
docker build -t phantomgrid-osint .
docker run -p 8000:8000 phantomgrid-osint
```

API docs available at `http://localhost:8000/docs`

---

## API Endpoints

### System

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API status and intel count |
| GET | `/health` | Health check |

### Intelligence Operations

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/scan` | Execute an OSINT scan against target domains |
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

---

## Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11+ |
| Framework | FastAPI |
| HTTP Client | aiohttp |
| Validation | Pydantic |
| Testing | pytest |
| Linting | ruff |
| Container | Docker |

---

## Project Structure

```
PhantomGrid-OSINT-Lab/
├── api/
│   └── main.py           # FastAPI application with OSINT engine
├── tests/                # Unit tests
├── docs/                 # Documentation
├── index.html            # Static frontend
├── Dockerfile            # Container build
├── .dockerignore         # Docker build exclusions
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata and build config
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

---

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check api/
ruff format api/ --check
```

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Part of the <a href="https://github.com/Raphasha27">Kirov Dynamics Technology</a> portfolio
</div>

<!-- 2026-08-31 17:04:23 -->

<!-- trigger-170843 -->
