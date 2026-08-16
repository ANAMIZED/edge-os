"""Edge OS MCP Server — expose funding detection + risk as MCP tools."""
from __future__ import annotations
from typing import Any, List, Optional
from edge_os.sdk.client import EdgeOSClient
from edge_os.models import Venue, FundingOpportunity
from edge_os.risk.guardian import PortfolioState

try:
    from mcp.server import MCPServer
    mcp = MCPServer(
        "Edge OS",
        instructions=(
            "You are connected to Edge OS, an Autonomous Agentic Operating System for RWA perps arbitrage. "
            "Use tools to detect funding opportunities, evaluate risk, and inspect portfolio state. "
            "Always prefer fail-closed risk limits (2-5x leverage, dual-leg buffers)."
        ),
    )
except ImportError:
    # graceful when mcp not installed
    class _Dummy:
        def tool(self, *a, **k):
            def deco(f): return f
            return deco
        def run(self): pass
    mcp = _Dummy()

_client = EdgeOSClient()

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

def main() -> None:
    mcp.run()

if __name__ == "__main__":
    main()
