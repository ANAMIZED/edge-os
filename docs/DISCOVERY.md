# Edge OS — Discovery Notes

## Domain
RWA perpetual futures arbitrage (tokenized equities, commodities, forex, pre-IPO) across CEX and DEX venues.

## Demand & Gaps (from team research, Aug 2026)
- Explosive volume ($470B–$708B monthly).
- Structural edges: funding/rollover differentials (Ostium real-carry vs speculative), weekend/off-hours basis, Lighter zero-fee legs, Hyperliquid discovery, CEX depth.
- Gaps: fragmented oracles, thin long-tail liquidity, capital mobility frictions, oracle risk (Ostium July 2026 incident), weekend gaps.

## Standards & Constraints
- Fail-closed risk (2–5x max leverage, dual-leg buffers).
- Prefer offline/mock paths for verification.
- Multi-surface agentic product (kernel = models + risk + scanner; surfaces = future CLI/API/MCP/skills).

## Key Insights Captured
Preferred pairings, annualization of 1h/8h rates, net-APR scoring after fees, oracle-health gates, concentration limits.
