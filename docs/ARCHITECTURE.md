# PhantomGrid OSINT Lab — Architecture

## System Overview

PhantomGrid OSINT Lab is an autonomous cyber intelligence and threat aggregation engine built with FastAPI. It simulates Open Source Intelligence (OSINT) scraping, threat actor tracking, IoC (Indicators of Compromise) generation, and real-time cyber alerting — all with synthetic data in an isolated lab environment.

## Architecture Diagram

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
│  │ ┌────────┐ │ │
│  │ │ Scanner│ │ │
│  │ │ IoC Gen│ │ │
│  │ │ Actors │ │ │
│  │ │ Alerts │ │ │
│  │ └────────┘ │ │
│  └─────┬──────┘ │
└────────┼────────┘
         │
    ┌────▼────────────┐
    │  In-Memory Store │
    │  (Synthetic Data)│
    └─────────────────┘
```

## Technology Stack

| Component      | Technology        | Version  |
|----------------|-------------------|----------|
| Language       | Python            | 3.11+    |
| Framework      | FastAPI           | —        |
| HTTP Client    | aiohttp           | —        |
| Validation     | Pydantic          | —        |
| Testing        | pytest            | —        |
| Linting        | ruff              | —        |
| Container      | Docker            | —        |
| Deployment     | Vercel            | —        |

## Directory Structure

```
PhantomGrid-OSINT-Lab/
├── api/
│   ├── main.py            # FastAPI application with OSINT engine
│   └── index.py           # Vercel serverless entrypoint
├── tests/                 # Unit tests
├── docs/                  # Documentation
├── index.html             # Static frontend
├── osint_dump.json        # Sample OSINT data dump
├── Dockerfile             # Container build
├── .dockerignore          # Docker build exclusions
├── vercel.json            # Vercel deployment config
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project metadata
├── .pre-commit-config.yaml
├── CONTRIBUTING.md
├── SECURITY.md
├── CODE_OF_CONDUCT.md
└── LICENSE
```

## Data Flow

### OSINT Scan
1. Client sends `POST /api/v1/scan` with target domain, depth, and keywords.
2. OSINT engine simulates scraping across surface web, dark web stubs.
3. IoCs extracted: IP addresses, TTPs (TTP IDs), domains, hashes.
4. Intelligence entries created with severity scores.
5. Critical alerts (severity >= 7) flagged for immediate attention.

### Threat Actor Profiling
1. `GET /api/v1/actors` returns APT group profiles.
2. Each actor has: name, aliases, severity, attack vectors, associated IoCs.
3. Cross-referenced with scan results for attribution.

### IoC Feed
1. `GET /api/v1/ioc` returns standardized IoC feed.
2. Format compatible with SIEM integration (STIX-like structure).
3. Filterable by type (IP, domain, hash, TTP) and severity.

### Alert System
1. `GET /api/v1/alerts` returns critical alerts (severity >= 7).
2. Real-time feed for high-priority threats.
3. Aggregated from all scan results and actor intelligence.

## Security

- **Isolated lab environment**: No production database connections, no live DNS, no real threat data.
- **Synthetic data only**: All IoCs and threat actors are simulated.
- **No network scanning**: OSINT engine uses synthetic data, not real reconnaissance.
- **CORS enabled**: Ready for frontend integration with configurable origins.
- **Environment variables**: Configuration via `.env` file.

## Deployment

### Docker

```bash
docker build -t phantomgrid-osint .
docker run -p 8000:8000 phantomgrid-osint
```

### Vercel (Serverless)

```bash
vercel deploy
```

### Local Development

```bash
cp .env.example .env
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

### API Endpoints

| Method | Path                  | Description                           |
|--------|-----------------------|---------------------------------------|
| GET    | `/`                   | API status and intel count            |
| GET    | `/health`             | Health check                          |
| POST   | `/api/v1/scan`        | Execute OSINT scan                    |
| GET    | `/api/v1/intel`       | List intel entries (filter by severity)|
| GET    | `/api/v1/intel/{id}`  | Get specific intel entry              |
| GET    | `/api/v1/actors`      | Threat actor profiling                |
| GET    | `/api/v1/alerts`      | Critical alerts (severity >= 7)       |
| GET    | `/api/v1/ioc`         | Indicators of Compromise feed         |

## Scaling Considerations

- **In-memory store**: Replace with Redis/PostgreSQL for persistence across restarts.
- **Async scanning**: Use Celery/background tasks for long-running OSINT scans.
- **Rate limiting**: Implement per-IP scan limits to prevent abuse.
- **Data enrichment**: Integrate with real OSINT APIs (VirusTotal, Shodan) for production.
- **Webhook alerts**: Push critical alerts to Slack, PagerDuty, or SIEM via webhooks.
- **Multi-tenant**: Add workspace isolation for team-based intelligence sharing.

## Decision Records

| Decision | Rationale |
|----------|-----------|
| Synthetic data | Avoids legal/ethical issues with real OSINT; demonstrates platform capabilities |
| In-memory store | Zero-config for lab environment; fast iteration without DB setup |
| FastAPI | Async support for concurrent scans; auto-generated API docs |
| aiohttp for HTTP | Async HTTP client for non-blocking simulated scraping |
| Vercel deployment | Serverless-first design; scales to zero when not in use |
| STIX-like IoC format | Industry standard for threat intelligence sharing; SIEM-compatible |
