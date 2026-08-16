# AGENTS.md — Edge OS

This file is the contract for any AI coding agent working on this repository.

## What this project is

Edge OS is an Autonomous Agentic Operating System specialized for RWA perpetual futures arbitrage (funding, basis, weekend gaps) across CEX/DEX venues (Hyperliquid, Lighter, Binance, Ostium, etc.).
It treats detection, risk, and execution agents as first-class processes with fail-closed risk limits derived from 2026 market research.

A senior engineer with only the source code and README.md must be able to install, run an offline mock scan, and verify end-to-end via `scripts/verify.sh`.

## How to run & verify

```bash
pip install -e .
bash scripts/verify.sh
```

## Hard rules for agents

1. Never break the verify contract.
2. Fail closed (risk gates, leverage 2-5x max, dual-leg buffers).
3. Prefer offline/mock paths for verification.
4. Keep research-aligned pairings (Lighter + HL/Binance priority).
5. Do not add external network calls to the default/mock path.
6. Prefer small, focused changes. Update README.md and AGENTS.md when public surfaces change.

## Surfaces that must stay working

Package (edge_os), RiskGuardian, FundingScanner/Detector, scripts/verify.sh, skills/, AGENTS.md
