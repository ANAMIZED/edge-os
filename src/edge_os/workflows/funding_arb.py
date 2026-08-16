"""Multi-agent style funding-arb workflow (offline)."""
from __future__ import annotations
from typing import Any, Dict, List
from edge_os.sdk.client import EdgeOSClient
from edge_os.models import NormalizedMarket, Venue, AssetClass
from edge_os.risk.guardian import PortfolioState

def run_funding_arb_workflow(available_capital: float = 50_000.0) -> Dict[str, Any]:
    """Simple multi-step workflow: detect → risk → size."""
    client = EdgeOSClient()
    # Mock markets
    markets = [
        NormalizedMarket(venue=Venue.LIGHTER, symbol="XAU-USDC", base_asset="XAU", asset_class=AssetClass.COMMODITY,
                         mark_price=2400.0, funding_rate=0.00005, funding_interval_hours=1.0, funding_apr=0.438,
                         open_interest=8e6, max_leverage=15.0),
        NormalizedMarket(venue=Venue.HYPERLIQUID, symbol="XAU-USDC", base_asset="XAU", asset_class=AssetClass.COMMODITY,
                         mark_price=2401.0, funding_rate=0.0002, funding_interval_hours=1.0, funding_apr=1.752,
                         open_interest=12e6, max_leverage=20.0),
    ]
    opps = client.detect_opportunities(markets)
    results = []
    port = PortfolioState(total_equity=available_capital)
    for opp in opps:
        approved = client.evaluate_risk(opp, port, available_capital)
        results.append({
            "opportunity": opp.model_dump(mode="json"),
            "approved": approved.model_dump(mode="json") if approved else None,
        })
    return {"workflow": "funding_arb", "results": results, "status": "completed"}
