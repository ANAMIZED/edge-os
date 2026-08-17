---
name: multi-agent-workflow
description: Run Edge OS multi-agent funding-arb workflows (scan → quant → risk → dual-leg).
---

# Multi-agent workflow (Edge OS)

## When to use
- Funding-rate / basis opportunity scan under RiskGuardian
- Coordinated detector → sizer → risk → execution agents

## Entry points
- Python: `from edge_os.workflows import run_funding_arb_workflow`
- CLI: `python -m edge_os.cli scan`
- API: `POST /v1/workflows/funding-arb`
- MCP: tools exposed by `edge-os-mcp`

## Contract
Fail closed. Offline/mock preferred for verification.
