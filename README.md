# PolyBot — Complete Engineering Blueprint

**A Full Build Plan for a Polymarket Closing Window Scanner**

---

## Overview
PolyBot is a sophisticated scanner designed to identify Polymarket events within their closing windows, applying various filters and scoring mechanisms to find optimal entry points.

## Project Structure
The project is organized into several modules:
- `polybot/scanner`: Core scanning logic, including fetching, filtering, and scoring.
- `polybot/sources`: External data sources for market validation (Weather, TSA, CDC).
- `polybot/notifier`: Telegram notification system.
- `polybot/display`: Terminal UI components using Rich.
- `polybot/scheduler`: Automated scanning loops.
- `polybot/trader`: Polymarket CLOB interaction and order management.

## Getting Started
### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation
```bash
git clone https://github.com/adrien-bot1/polymarket.git
cd polymarket
cp .env.example .env
# Fill in your credentials in .env
uv sync --all-extras
```

### Usage
```bash
uv run polybot
```

## Features
- **Closing Window Scanner**: Finds markets ending in 6-72 hours.
- **Liquidity & Volume Filters**: Ensures markets have sufficient depth.
- **Scoring Engine**: Ranks markets based on price trends and external data.
- **Telegram Alerts**: Real-time notifications for high-scoring opportunities.
- **Dual-Mode Execution**: Support for both manual signals and semi-automated trading.
