---
name: funding-arb
description: Detect and risk-gate RWA perpetual funding-rate arbitrage opportunities across preferred venue pairings.
version: 0.1.0
license: Apache-2.0
tags: [funding, arbitrage, rwa, edge-os, risk]
---

# Funding Arb Skill

Use Edge OS kernel (FundingSpreadDetector + RiskGuardian) to surface net-positive funding spreads under 2-5x leverage and dual-leg buffers.

Prefer Lighter zero-fee legs and Ostium stable rollover baselines.
