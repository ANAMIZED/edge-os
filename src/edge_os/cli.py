"""Edge OS CLI — operator surface."""
from __future__ import annotations
import json
import typer
from rich import print as rprint
from rich.table import Table
from edge_os.sdk.client import EdgeOSClient
from edge_os.models import Venue, FundingOpportunity, RiskLimits
from edge_os.risk.guardian import PortfolioState
from datetime import datetime

app = typer.Typer(name="edge-os", help="Edge OS — RWA Perps Agentic Operating System CLI", no_args_is_help=True)

@app.command()
def version():
    rprint("Edge OS 0.1.0")

@app.command()
def status():
    """Show kernel health."""
    c = EdgeOSClient()
    h = c.health()
    rprint(f"[green]OK[/green]  {h}")

@app.command()
def scan(mock: bool = typer.Option(True, "--mock/--live")):
    """Run funding opportunity scan (mock by default)."""
    c = EdgeOSClient()
    # Minimal mock markets for offline demo
    from edge_os.models import NormalizedMarket, AssetClass
    markets = [
        NormalizedMarket(venue=Venue.LIGHTER, symbol="XAU-USDC", base_asset="XAU", asset_class=AssetClass.COMMODITY,
                         mark_price=2400.0, funding_rate=0.00005, funding_interval_hours=1.0, funding_apr=0.438,
                         open_interest=8e6, max_leverage=15.0),
        NormalizedMarket(venue=Venue.HYPERLIQUID, symbol="XAU-USDC", base_asset="XAU", asset_class=AssetClass.COMMODITY,
                         mark_price=2401.0, funding_rate=0.0002, funding_interval_hours=1.0, funding_apr=1.752,
                         open_interest=12e6, max_leverage=20.0),
    ]
    opps = c.detect_opportunities(markets)
    if not opps:
        rprint("No opportunities above threshold.")
        return
    table = Table(title="Funding Opportunities")
    table.add_column("Asset")
    table.add_column("Long")
    table.add_column("Short")
    table.add_column("Net APR")
    for o in opps:
        table.add_row(o.asset, o.long_venue.value, o.short_venue.value, f"{o.estimated_net_apr*100:.1f}%")
    rprint(table)

@app.command()
def risk_check():
    """Smoke-test RiskGuardian."""
    c = EdgeOSClient()
    opp = FundingOpportunity(
        asset="XAU", long_venue=Venue.LIGHTER, short_venue=Venue.HYPERLIQUID,
        long_funding_apr=0.05, short_funding_apr=0.25, gross_spread_apr=0.20,
        estimated_net_apr=0.15, long_oi=5e6, short_oi=5e6,
        liquidity_score=0.8, risk_score=0.3, recommended_leverage=3.0
    )
    approved = c.evaluate_risk(opp)
    if approved:
        rprint(f"[green]Approved[/green] notional={approved.approved_notional:.0f} lev={approved.approved_leverage}")
    else:
        rprint("[red]Rejected[/red]")

if __name__ == "__main__":
    app()
