# Edge OS — Synthesis

## Product Identity
Autonomous Agentic Operating System specialized for delta-neutral RWA perpetual futures arbitrage.
Agents as processes that discover, size, and (paper/live) execute funding, basis, and related strategies under strict risk controls derived from live 2026 market research.
Optional AQuA-style research loop (arXiv:2608.12841) enables bounded recursive self-improvement of detection/ranking via sealed evaluation and validated beliefs.

## Declared Surfaces
- Kernel: models, FundingScanner, RiskGuardian, DryRun execution, BeliefStore, ResearchLoop / SealedEvaluator
- Package: `edge_os` importable Python library
- SDK / CLI / MCP / Workflows
- Verify: `scripts/verify.sh` (stranger-runnable, offline preferred)
- Skills: discovery-distribution, funding-arb, aqua-research
- AGENTS.md contract

## Acceptance Contract
A senior engineer with only the repository and README can:
1. Install / run offline mock scan and AQuA-style research loop
2. Execute `bash scripts/verify.sh` and see green checks across all surfaces
3. Observe scored funding opportunities with research-aligned pairings, risk gates, and optional belief consultation

## Governance (AQuA Alignment)
- Sealed sandbox for research agents (fixed splits, immutable evaluator)
- Asymmetric freedom: research may propose and validate; live path remains fail-closed and opt-in for beliefs
- No ambient authority from research to capital or risk limits
- Citation: AQuA — Recursively Self-Improving Quantitative Trading Research Agents (arXiv:2608.12841)

Fail-closed: no live capital without explicit progressive unlock and kill switches.
