# PhantomGrid OSINT Lab

**Autonomous Cyber Intelligence & Scraping Bot** — an experimental cybersecurity repository for Open Source Intelligence (OSINT) gathering and analysis.

## Overview

PhantomGrid automates the collection, processing, and correlation of publicly available intelligence from diverse sources. Designed for security researchers, threat analysts, and CTF participants.

## Features

- **Multi-source Collection:** Scraping from web, social media, dark web indexes, and public APIs
- **Intelligence Correlation:** Cross-reference indicators across data sources
- **Automated Reporting:** Generate structured OSINT reports in JSON/PDF
- **Modular Architecture:** Pluggable collectors for extensibility

## Tech Stack

- **Language:** Python 3.12
- **Web Scraping:** Playwright, BeautifulSoup, Scrapy
- **Data Processing:** Pandas, NLP (spaCy)
- **Storage:** SQLite / PostgreSQL
- **Orchestration:** Docker, GitHub Actions

## Getting Started

```bash
git clone https://github.com/Raphasha27/PhantomGrid-OSINT-Lab.git
cd PhantomGrid-OSINT-Lab
pip install -r requirements.txt
python phantomgrid.py --collect --sources twitter,news,shodan
```

## Project Structure

```
+-- collectors/        # Source-specific data collectors
+-- analyzers/         # Intelligence analysis modules
+-- reporters/         # Report generation & export
+-- config/            # Collector & pipeline configuration
+-- data/              # Collected intelligence storage
+-- tests/             # Unit tests
+-- phantomgrid.py     # Main entry point
```

## Usage

```bash
# Collect intelligence from specified sources
python phantomgrid.py --collect --sources all

# Analyze collected data
python phantomgrid.py --analyze --report threat_brief

# Generate PDF report
python phantomgrid.py --report --format pdf --output /tmp/report.pdf
```

## Legal & Ethical Use

This tool is intended for **legal and ethical OSINT purposes only**. Users are responsible for complying with applicable laws and platform terms of service.

## Security

Report vulnerabilities: 402106633@my.richfield.ac.za

## License

Experimental security research project — Raphasha27
