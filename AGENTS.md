# AGENTS.md — Edge OS

This file is the contract for any AI coding agent working on this repository.

## What this project is

Edge OS is an Autonomous Agentic Operating System specialized for Real-World Asset (RWA) perpetual futures arbitrage.

It runs specialized agents (data/scanner, risk guardian, execution, orchestrator) under strict research-derived risk limits, fail-closed defaults, and a paper-first progression.

A senior engineer with only the source code and README.md must be able to understand the system, run it in paper mode, and verify end-to-end via `bash scripts/verify.sh`.

## How to run & verify

```bash
# From repo root
python -m pip install -e .   # or pip install -r requirements.txt
bash scripts/verify.sh
```

## Hard rules for agents

1. Never break the verify contract.
2. Fail closed — paper mode is the default; live requires explicit opt-in.
3. Respect the research risk envelope: max 5x leverage, preferred 2–3x, dual-leg buffer, oracle health ≥ 0.85, weekend size reduction.
4. Prefer fee-efficient legs (Lighter) and stable-carry legs (Ostium) when ranking opportunities.
5. No ambient authority. All venue keys, capital limits, and live flags must be explicit configuration.
6. Do not add external network calls to the default/mock/verify path.
7. Prefer small, focused changes. Update README.md, AGENTS.md, and SYNTHESIS.md when public surfaces change.
8. Keep Discovery → Synthesis → Build → Verify → Elite → Distribute discipline.

## Surfaces that must stay working

- Kernel models (`src/edge_os/models.py`)
- FundingScanner (offline/mock capable)
- RiskGuardian
- DryRun execution
- Orchestrator paper loop
- `scripts/verify.sh`
- AGENTS.md + skills/

## Domain context (short)

Primary strategy for MVP: cross-venue funding rate arbitrage on liquid RWA perps (XAU, NVDA, oil, major indices).
Preferred pairings: Lighter + Hyperliquid/Binance; Ostium + high-funding orderbooks.
Full research and risk rules live in docs/ and config/.
