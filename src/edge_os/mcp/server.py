"""Edge OS MCP Server — funding detection, risk, and AQuA-style research tools."""
from __future__ import annotations
from typing import Any, List, Optional
from edge_os.sdk.client import EdgeOSClient
from edge_os.models import Venue, FundingOpportunity
from edge_os.memory.beliefs import BeliefStore
from edge_os.research.workflow import run_aqua_research_loop

try:
    from mcp.server import MCPServer
    mcp = MCPServer(
        "Edge OS",
        instructions=(
            "You are connected to Edge OS, an Autonomous Agentic Operating System for RWA perps arbitrage. "
            "Use tools to detect funding opportunities, evaluate risk, run offline AQuA-style research loops, "
            "and manage validated beliefs. Always prefer fail-closed risk limits (2-5x leverage, dual-leg buffers). "
            "Research tools are sealed/offline only; never grant ambient authority to live capital."
        ),
    )
except ImportError:
    class _Dummy:
        def tool(self, *a, **k):
            def deco(f): return f
            return deco
        def run(self): pass
    mcp = _Dummy()

_client = EdgeOSClient()
_beliefs = BeliefStore()

@mcp.tool()
def health() -> dict[str, Any]:
    """Return Edge OS kernel health."""
    return _client.health()

@mcp.tool()
def list_priority_pairings() -> List[str]:
    """Return preferred venue pairings from research."""
    return [
        "Lighter + Hyperliquid",
        "Lighter + Binance",
        "Ostium + Hyperliquid",
        "Ostium + Binance",
        "Hyperliquid + Binance",
    ]

@mcp.tool()
def evaluate_sample_opportunity() -> dict[str, Any]:
    """Run RiskGuardian on a sample XAU opportunity (offline)."""
    opp = FundingOpportunity(
        asset="XAU", long_venue=Venue.LIGHTER, short_venue=Venue.HYPERLIQUID,
        long_funding_apr=0.05, short_funding_apr=0.25, gross_spread_apr=0.20,
        estimated_net_apr=0.15, long_oi=5e6, short_oi=5e6,
        liquidity_score=0.8, risk_score=0.3, recommended_leverage=3.0
    )
    approved = _client.evaluate_risk(opp)
    if approved is None:
        return {"status": "rejected"}
    return {
        "status": "approved",
        "notional": approved.approved_notional,
        "leverage": approved.approved_leverage,
        "reasons": approved.reasons,
    }

@mcp.tool()
def edge_research_propose() -> List[dict[str, str]]:
    """Manager: propose AQuA-style research hypotheses (offline)."""
    from edge_os.research.workflow import _manager_propose
    return _manager_propose()

@mcp.tool()
def edge_research_evaluate() -> dict[str, Any]:
    """Run sealed evaluation path via full research loop (offline)."""
    return run_aqua_research_loop(_beliefs)

@mcp.tool()
def edge_belief_update() -> dict[str, Any]:
    """Run full offline research loop and return validated beliefs."""
    return run_aqua_research_loop(_beliefs)

@mcp.tool()
def list_beliefs() -> List[dict[str, Any]]:
    """Dump current validated belief store."""
    return _beliefs.dump()

def main() -> None:
    mcp.run()

if __name__ == "__main__":
    main()
