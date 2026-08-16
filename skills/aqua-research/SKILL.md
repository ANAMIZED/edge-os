---
name: aqua-research
description: Optional AQuA-style recursive research loop for Edge OS. Offline/paper only. Manager proposes hypotheses about funding differentials, OI imbalances, weekend gaps, oracle lag; specialists convert to constrained expressions; sealed evaluator scores on historical data; validated beliefs written to persistent memory for optional consultation by live FundingScanner and RiskGuardian.
---

# AQuA-Style Research Skill (Edge OS)

## Purpose
Provide bounded recursive self-improvement of detection and ranking logic without touching the sealed live/paper execution path.

Inspired by AQuA (arXiv:2608.12841): manager-mediated multi-agent research, sealed sandbox, evidence retention.

## When to use
- User or orchestrator requests research / hypothesis generation on RWA funding, basis, gaps, oracles.
- Offline or paper mode only.
- Never for live capital decisions.

## Workflow
1. **Manager** proposes hypotheses (funding differentials, OI imbalance, weekend gaps, oracle lag).
2. **Specialists** convert hypotheses into constrained expressions or ranking configs.
3. **Sealed evaluator** scores candidates on fixed historical funding + mark/index splits (offline mock or recorded data).
4. **Belief write-back**: validated results → Belief / Evidence Memory store.
5. Live FundingScanner and RiskGuardian may *optionally* consult the store; default path remains independent and fail-closed.

## MCP tools
- `edge_research_propose`
- `edge_research_evaluate`
- `edge_belief_update`

## Hard constraints
- Offline / paper only.
- Sealed sandbox: no mutation of live data splits, labels, or evaluators.
- No ambient authority over capital or risk limits.
- Asymmetry principle (AQuA + Edge OS): agents act only through constrained interfaces.

## References
- docs/SYNTHESIS.md, AGENTS.md
- src/edge_os/research/ (when present)
- src/edge_os/mcp/server.py
- arXiv:2608.12841
