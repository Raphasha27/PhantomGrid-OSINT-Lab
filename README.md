<div align="center">

# PhantomGrid OSINT Lab

**Autonomous Cyber Intelligence & Threat Aggregation Engine with IoC Tracking**

[![CI](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Quality](https://img.shields.io/badge/code%20quality-ruff-4B2E83)](https://docs.astral.sh/ruff/)
[![Test Coverage](https://img.shields.io/badge/test%20coverage-90%25-brightgreen)](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)](https://github.com/Raphasha27/PhantomGrid-OSINT-Lab)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi&logoColor=white)

</div>

---

## Features

- **IoC Extraction** — Automated Indicators of Compromise generation (IPs, TTPs, domains)
- **Domain/IP Correlation** — Cross-reference IOCs across multiple source domains
- **Threat Actor Profiling** — Track APT groups with severity and attack vector analysis
- **Dark Web Monitoring Stub** — Simulated .onion source aggregation for lab use
- **Feed Aggregation** — Standardised IoC feed export for SIEM integration
- **Real-time Alerting** — Critical alert feed for high-severity threats (severity ≥ 7)
- **API-First Design** — Full REST API with OpenAPI documentation
- **CORS Enabled** — Ready for frontend dashboard integration

---

## Quick Start

```bash
git clone https://github.com/Raphasha27/PhantomGrid-OSINT-Lab.git
cd PhantomGrid-OSINT-Lab
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

API docs (Swagger UI): `http://localhost:8000/docs`

### Docker

```bash
docker build -t phantomgrid-osint .
docker run -p 8000:8000 phantomgrid-osint
```

---

## Architecture

> Full architecture documentation: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

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

## API Documentation

> Full API reference: [docs/API.md](docs/API.md) · Swagger UI: `http://localhost:8000/docs`

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
| GET | `/api/v1/alerts` | Critical alerts (severity ≥ 7) |
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

| Component | Technology | Description |
|-----------|------------|-------------|
| Language | Python 3.11+ | Core runtime |
| Framework | FastAPI | Async REST API |
| HTTP Client | aiohttp | Async HTTP requests |
| Validation | Pydantic | Request/response schemas |
| Data Store | In-memory dict | Synthetic data (lab only) |
| Testing | pytest | Unit and integration tests |
| Linting | ruff | Fast Python linter |
| Container | Docker | Single-container deployment |

---

## Project Structure

```
PhantomGrid-OSINT-Lab/
├── api/
│   └── main.py           # FastAPI application with OSINT engine
├── tests/                # Unit tests
├── docs/
│   ├── ARCHITECTURE.md
│   └── API.md
├── index.html            # Static frontend
├── Dockerfile            # Container build
├── .dockerignore         # Docker build exclusions
├── requirements.txt      # Python dependencies
├── pyproject.toml        # Project metadata and build config
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── LICENSE
└── README.md
```

---

## Testing

```bash
pip install -e ".[dev]"
pytest --cov=api --cov-report=term-missing -v
ruff check api/
ruff format api/ --check
```

---

## Deployment

### Docker

```bash
docker build -t phantomgrid-osint .
docker run -d -p 8000:8000 --name phantomgrid phantomgrid-osint
docker logs phantomgrid    # View logs
docker stop phantomgrid     # Stop container
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PORT` | `8000` | FastAPI server port |
| `LOG_LEVEL` | `info` | Logging verbosity |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |
| `MAX_SCAN_DEPTH` | `3` | Maximum OSINT scan depth |

### Local Development

```bash
pip install -e ".[dev]"
uvicorn api.main:app --reload --port 8000
```

---

## Security

> **Safety Protocol**: Isolated lab environment. No production database connections, no live DNS routing, no real threat data.

See [SECURITY.md](SECURITY.md) for responsible disclosure guidelines.

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue before submitting a PR.

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Part of the <a href="https://github.com/Raphasha27">Kirov Dynamics Technology</a> portfolio
</div>
