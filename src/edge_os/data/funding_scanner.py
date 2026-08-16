"""
Funding Scanner Agent - Core data ingestion & opportunity detection for funding rate arb.
Assigned to Lucas.

Normalizes rates across venues with different intervals (1h vs 8h),
computes annualized APRs and net spreads after estimated fees,
prioritizes preferred pairings (Lighter + HL/Binance, Ostium + orderbooks).
"""

from typing import List, Dict, Optional
from datetime import datetime
import asyncio
from edge_os.models import (
    Venue, NormalizedMarket, FundingOpportunity, AssetClass, RiskLimits
)

# Placeholder for real API clients
# from edge_os.data.clients import HyperliquidClient, BinanceClient, LighterClient, OstiumClient

class FundingScanner:
    """
    Continuously fetches, normalizes, and ranks funding rate opportunities
    across priority RWA venues.
    """

    def __init__(self, risk_limits: Optional[RiskLimits] = None):
        self.risk_limits = risk_limits or RiskLimits()
        self.priority_assets = [
            "XAU", "XAG", "WTI", "BRENT",  # commodities
            "NVDA", "TSLA", "AAPL", "MU", "SNDK", "SKHYNIX",  # equities / memory
            "SPY", "QQQ", "SPX", "NDX",  # indices
            "SPCX",  # pre-IPO example
            "EUR", "USDJPY"  # forex
        ]
        self.preferred_pairings = [
            (Venue.LIGHTER, Venue.HYPERLIQUID),
            (Venue.LIGHTER, Venue.BINANCE),
            (Venue.OSTIUM, Venue.HYPERLIQUID),
            (Venue.OSTIUM, Venue.BINANCE),
            (Venue.HYPERLIQUID, Venue.BINANCE),
            (Venue.LIGHTER, Venue.BYBIT),
            # etc.
        ]

    def annualize_funding(self, rate: float, interval_hours: float) -> float:
        """Convert raw funding rate to approximate annualized APR.
        rate is the payment rate for the interval (e.g. 0.0001 for 0.01%).
        """
        if interval_hours <= 0:
            return 0.0
        periods_per_year = (365 * 24) / interval_hours
        return rate * periods_per_year

    def estimate_net_spread(
        self,
        long_apr: float,
        short_apr: float,
        long_taker_fee: float,
        short_taker_fee: float,
        hold_days: float = 7.0
    ) -> float:
        """Rough net APR after round-trip fees amortized over hold period.
        Assumes one entry/exit. More sophisticated models can add slippage, funding variance.
        """
        gross = short_apr - long_apr  # positive if short has higher positive funding (or long more negative)
        # Fees: open + close on both legs ≈ 2 * (long_fee + short_fee)
        fee_cost = 2 * (long_taker_fee + short_taker_fee)
        # Amortize fee cost over hold period as APR equivalent
        fee_apr_equiv = fee_cost * (365 / hold_days)
        return gross - fee_apr_equiv

    async def fetch_markets(self) -> List[NormalizedMarket]:
        """Fetch and normalize from priority venues. Replace with real clients."""
        # TODO: Implement real async fetches
        # hl = await HyperliquidClient().get_rwa_markets()
        # bn = await BinanceClient().get_rwa_markets()
        # lt = await LighterClient().get_rwa_markets()
        # ...
        # For now return empty; will be populated in live version
        return []

    def detect_opportunities(
        self, markets: List[NormalizedMarket]
    ) -> List[FundingOpportunity]:
        """Group by asset and find best long/short pairs."""
        by_asset: Dict[str, List[NormalizedMarket]] = {}
        for m in markets:
            if m.base_asset not in by_asset:
                by_asset[m.base_asset] = []
            by_asset[m.base_asset].append(m)

        opps: List[FundingOpportunity] = []
        for asset, venue_markets in by_asset.items():
            if len(venue_markets) < 2:
                continue
            # Sort by funding_apr ascending (lowest first = best to long)
            venue_markets.sort(key=lambda x: x.funding_apr)
            for i, long_m in enumerate(venue_markets):
                for short_m in venue_markets[i+1:]:
                    gross = short_m.funding_apr - long_m.funding_apr
                    if gross < self.risk_limits.min_net_apr_threshold * 0.5:
                        continue  # rough pre-filter
                    net = self.estimate_net_spread(
                        long_m.funding_apr, short_m.funding_apr,
                        long_m.taker_fee, short_m.taker_fee
                    )
                    if net < self.risk_limits.min_net_apr_threshold:
                        continue
                    # Liquidity score simple: log OI weighted
                    liq = min(1.0, (long_m.open_interest + short_m.open_interest) / 50_000_000)
                    # Risk score placeholder (oracle, venue risk, etc.)
                    risk = 0.3
                    if long_m.venue == Venue.OSTIUM or short_m.venue == Venue.OSTIUM:
                        risk += 0.1  # post-exploit caution
                    if "HIP" in str(long_m.extra) or "HIP" in str(short_m.extra):
                        risk += 0.1  # builder oracle

                    opp = FundingOpportunity(
                        asset=asset,
                        long_venue=long_m.venue,
                        short_venue=short_m.venue,
                        long_funding_apr=long_m.funding_apr,
                        short_funding_apr=short_m.funding_apr,
                        gross_spread_apr=gross,
                        estimated_net_apr=net,
                        long_oi=long_m.open_interest,
                        short_oi=short_m.open_interest,
                        liquidity_score=liq,
                        risk_score=risk,
                        recommended_leverage=min(self.risk_limits.preferred_leverage, self.risk_limits.max_leverage),
                        notes=f"Preferred pairing check: {(long_m.venue, short_m.venue) in self.preferred_pairings or (short_m.venue, long_m.venue) in self.preferred_pairings}"
                    )
                    opps.append(opp)

        # Rank by net_apr * liq / (1 + risk)
        opps.sort(key=lambda o: (o.estimated_net_apr * o.liquidity_score) / (1 + o.risk_score), reverse=True)
        return opps

    async def run_scan_cycle(self) -> List[FundingOpportunity]:
        markets = await self.fetch_markets()
        return self.detect_opportunities(markets)

# Example usage (to be integrated with Orchestrator)
async def main():
    scanner = FundingScanner()
    opps = await scanner.run_scan_cycle()
    for o in opps[:5]:
        print(o)

if __name__ == "__main__":
    asyncio.run(main())
