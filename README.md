# Edge OS

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Autonomous Agentic Operating System for RWA Perpetual Futures Arbitrage**

Edge OS continuously monitors, detects, sizes, and (in controlled modes) executes delta-neutral funding-rate, basis, and related strategies across Hyperliquid, Lighter, Binance, Ostium, Bybit, OKX and related venues.

A senior engineer who has never seen this repository can, using **only** the source code and this `README.md`:

1. Install the package
2. Run an offline mock scan
3. Verify end-to-end correctness via automated checks

No prior context or tribal knowledge required.

## Quick Start

```bash
pip install -e .
bash scripts/verify.sh
```

## Surfaces

| Surface | Entry |
|---------|-------|
| Package / Kernel | `from edge_os.models import ...` / RiskGuardian / FundingSpreadDetector |
| Verify | `bash scripts/verify.sh` |
| Skills | `skills/*/SKILL.md` |
| AGENTS.md | Coding-agent contract at repo root |
| Docs | `docs/DISCOVERY.md`, `docs/SYNTHESIS.md` |

## Design principles

1. Fail closed (RiskGuardian, leverage hard caps, dual-leg buffers)
2. Research-aligned (preferred pairings, 2-5x, oracle gates, weekend buffers)
3. Offline/mock preferred for verification
4. Deployable with zero tribal knowledge
5. Cost and risk are first-class

## License

Apache-2.0
