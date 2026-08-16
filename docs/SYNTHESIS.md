# Edge OS — Synthesis

## Product Identity
Autonomous Agentic Operating System specialized for delta-neutral RWA perpetual futures arbitrage.
Agents as processes that discover, size, and (paper/live) execute funding, basis, and related strategies under strict risk controls derived from live 2026 market research.

## Declared Surfaces (MVP)
- Kernel: models, FundingScanner, RiskGuardian, DryRun execution
- Package: `edge_os` importable Python library
- Verify: `scripts/verify.sh` (stranger-runnable, offline preferred)
- Skills: discovery-distribution + domain skills
- Future: CLI, REST API, MCP server, AGENTS.md contract, Web control plane

## Acceptance Contract
A stranger with only the repository and README can:
1. Install / run offline mock scan
2. Execute `bash scripts/verify.sh` and see green checks
3. Observe scored funding opportunities with research-aligned pairings and risk gates

Fail-closed: no live capital without explicit progressive unlock and kill switches.
