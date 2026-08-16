"""FundingSpreadDetector — priority pairings from RWA research."""
from __future__ import annotations
from typing import List, Dict
from edge_os.models import Venue, NormalizedMarket, FundingOpportunity

PRIORITY_PAIRINGS = [
    (Venue.LIGHTER, Venue.HYPERLIQUID),
    (Venue.LIGHTER, Venue.BINANCE),
    (Venue.OSTIUM, Venue.HYPERLIQUID),
    (Venue.OSTIUM, Venue.BINANCE),
    (Venue.HYPERLIQUID, Venue.BINANCE),
    (Venue.LIGHTER, Venue.BYBIT),
]

class FundingSpreadDetector:
    def __init__(self, min_net_apr: float = 0.08, min_oi: float = 1_000_000.0):
        self.min_net_apr = min_net_apr
        self.min_oi = min_oi

    def detect(self, markets: List[NormalizedMarket]) -> List[FundingOpportunity]:
        by_asset: Dict[str, Dict[Venue, NormalizedMarket]] = {}
        for m in markets:
            by_asset.setdefault(m.base_asset, {})[m.venue] = m

        opps: List[FundingOpportunity] = []
        for asset, vmap in by_asset.items():
            for long_v, short_v in PRIORITY_PAIRINGS:
                if long_v not in vmap or short_v not in vmap:
                    continue
                long_m = vmap[long_v]
                short_m = vmap[short_v]
                if long_m.funding_apr >= short_m.funding_apr:
                    long_m, short_m = short_m, long_m
                    long_v, short_v = short_v, long_v

                gross = short_m.funding_apr - long_m.funding_apr
                fee_est = 0.0 if Venue.LIGHTER in (long_v, short_v) else 0.03
                net = gross - fee_est - 0.02

                if net < self.min_net_apr:
                    continue
                if min(long_m.open_interest, short_m.open_interest) < self.min_oi:
                    continue

                liq = min(1.0, min(long_m.open_interest, short_m.open_interest) / 10_000_000)
                risk = 0.3
                if long_m.oracle_source and "builder" in str(long_m.oracle_source).lower():
                    risk += 0.2

                opps.append(
                    FundingOpportunity(
                        asset=asset,
                        long_venue=long_v,
                        short_venue=short_v,
                        long_funding_apr=long_m.funding_apr,
                        short_funding_apr=short_m.funding_apr,
                        gross_spread_apr=gross,
                        estimated_net_apr=net,
                        long_oi=long_m.open_interest,
                        short_oi=short_m.open_interest,
                        liquidity_score=liq,
                        risk_score=risk,
                        recommended_leverage=3.0,
                        notes="Priority pairing (Lighter zero-fee preferred)",
                    )
                )
        return sorted(opps, key=lambda o: o.estimated_net_apr, reverse=True)
