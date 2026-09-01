from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random, uuid
from datetime import datetime, timedelta
from typing import Optional, List

app = FastAPI(
    title="PhantomGrid OSINT API",
    description=(
        "Autonomous Open Source Intelligence (OSINT) scraping and cyber threat aggregation engine.\n\n"
        "## Features\n"
        "- **Threat Scanning** — Scan domains for threat intelligence indicators\n"
        "- **Intel Feed** — Browse and filter collected intelligence entries\n"
        "- **Actor Profiling** — Aggregate threat actor activity and attack vectors\n"
        "- **Alert System** — High-severity alert aggregation with severity thresholds\n"
        "- **IOC Feed** — Indicator of Compromise feed with TTP mappings\n\n"
        "## Data Model\n"
        "Each intel entry includes: threat actor, attack vector, target sector, severity (1-10), "
        "confidence score, IOCs, and MITRE ATT&CK TTPs."
    ),
    version="1.0.0",
    contact={
        "name": "PhantomGrid OSINT Support",
        "url": "https://github.com/Raphasha27/PhantomGrid-OSINT-Lab",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "Scan", "description": "Initiate OSINT scans against target domains"},
        {
            "name": "Intel",
            "description": "Browse and filter collected threat intelligence entries",
        },
        {"name": "Actors", "description": "Threat actor profiling and aggregation"},
        {"name": "Alerts", "description": "High-severity threat alert feeds"},
        {
            "name": "IOC",
            "description": "Indicator of Compromise feeds with TTP mappings",
        },
        {"name": "Health", "description": "Service health checks"},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory intel store ---
intel_store = []
DOMAINS = [
    "darkforum-alpha.onion",
    "pastebin-mirror.net",
    "leak-registry.io",
    "shadow-exchange.xyz",
    "threat-intel-hub.net",
]
THREAT_ACTORS = [
    "APT-28",
    "Lazarus Group",
    "Cozy Bear",
    "Fancy Bear",
    "SilverFish",
    "Unknown Actor",
]
ATTACK_VECTORS = [
    "Phishing",
    "Supply Chain",
    "Zero-Day Exploit",
    "Credential Stuffing",
    "Ransomware",
    "Social Engineering",
]
TARGETS = [
    "Financial Sector",
    "Government Infrastructure",
    "Healthcare",
    "Energy Grid",
    "Tech Startups",
    "Academic Institutions",
]


class ScanRequest(BaseModel):
    target_domain: Optional[str] = "surface_web"
    depth: Optional[int] = 1
    keywords: Optional[List[str]] = ["breach", "exploit", "credential"]


class AlertRequest(BaseModel):
    actor: Optional[str] = None
    vector: Optional[str] = None
    severity_min: Optional[int] = 3


def generate_intel():
    return {
        "id": str(uuid.uuid4())[:8],
        "source_domain": random.choice(DOMAINS),
        "threat_actor": random.choice(THREAT_ACTORS),
        "attack_vector": random.choice(ATTACK_VECTORS),
        "target_sector": random.choice(TARGETS),
        "severity": random.randint(1, 10),
        "confidence_score": round(random.uniform(0.55, 0.97), 2),
        "ioc": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "ttps": random.choice(["T1566", "T1190", "T1059", "T1486", "T1078"]),
        "discovered_at": (
            datetime.utcnow() - timedelta(hours=random.randint(0, 72))
        ).isoformat(),
        "status": random.choice(["ACTIVE", "MONITORING", "CONTAINED", "ESCALATED"]),
    }


# Seed initial intel
for _ in range(15):
    intel_store.append(generate_intel())


@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "platform": "PhantomGrid-OSINT",
        "intel_entries": len(intel_store),
    }


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/v1/scan")
def scan(req: ScanRequest):
    new_entries = random.randint(2, 8)
    results = []
    for _ in range(new_entries):
        entry = generate_intel()
        intel_store.append(entry)
        results.append(entry)
    return {
        "scan_id": str(uuid.uuid4())[:8],
        "target": req.target_domain,
        "depth": req.depth,
        "keywords_matched": req.keywords,
        "new_intel_entries": new_entries,
        "results": results,
        "scan_duration_ms": random.randint(800, 4500),
    }


@app.get("/api/v1/intel")
def list_intel(limit: int = 20, severity_min: int = 1):
    filtered = [i for i in intel_store if i["severity"] >= severity_min]
    filtered.sort(key=lambda x: x["severity"], reverse=True)
    return {"total": len(filtered), "entries": filtered[:limit]}


@app.get("/api/v1/intel/{intel_id}")
def get_intel(intel_id: str):
    entry = next((i for i in intel_store if i["id"] == intel_id), None)
    if not entry:
        raise HTTPException(404, f"Intel ID '{intel_id}' not found.")
    return entry


@app.get("/api/v1/actors")
def list_actors():
    actor_map = {}
    for entry in intel_store:
        a = entry["threat_actor"]
        if a not in actor_map:
            actor_map[a] = {"actor": a, "count": 0, "avg_severity": 0, "vectors": set()}
        actor_map[a]["count"] += 1
        actor_map[a]["avg_severity"] += entry["severity"]
        actor_map[a]["vectors"].add(entry["attack_vector"])
    for a in actor_map:
        actor_map[a]["avg_severity"] = round(
            actor_map[a]["avg_severity"] / actor_map[a]["count"], 2
        )
        actor_map[a]["vectors"] = list(actor_map[a]["vectors"])
    return {"threat_actors": list(actor_map.values())}


@app.get("/api/v1/alerts")
def get_alerts(severity_min: int = 7):
    alerts = [i for i in intel_store if i["severity"] >= severity_min]
    return {
        "critical_alerts": len(alerts),
        "alerts": sorted(alerts, key=lambda x: x["severity"], reverse=True),
    }


@app.get("/api/v1/ioc")
def ioc_feed():
    iocs = [
        {"ioc": i["ioc"], "type": "IPv4", "severity": i["severity"], "ttps": i["ttps"]}
        for i in intel_store
    ]
    return {"ioc_count": len(iocs), "feed": iocs}
