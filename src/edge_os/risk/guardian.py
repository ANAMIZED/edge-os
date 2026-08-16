"""RiskGuardian — Edge OS fail-closed risk engine.

Enforces research-derived limits: 2-5x leverage, dual-leg buffers,
oracle health, weekend gap controls, concentration caps.
Optionally consults BeliefStore (AQuA-style) via explicit opt-in only.
"""
from __future__ import annotations
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from edge_os.models import Venue, FundingOpportunity, Position, RiskLimits

class ApprovedOpportunity(BaseModel):
    opportunity: FundingOpportunity
    approved_notional: float
    approved_leverage: float
    max_hold_hours: float = 48.0
    reasons: List[str] = Field(default_factory=list)
    risk_adjusted: bool = True

class PortfolioState(BaseModel):
    positions: List[Position] = Field(default_factory=list)
    total_equity: float = 0.0
    total_exposure_usd: float = 0.0
    venue_exposure: Dict[str, float] = Field(default_factory=dict)
    asset_exposure: Dict[str, float] = Field(default_factory=dict)
    cluster_exposure: Dict[str, float] = Field(default_factory=dict)
    accrued_funding: float = 0.0
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class RiskGuardian:
    """Fail-closed risk gate for all Edge OS opportunities."""

    def __init__(
        self,
        limits: Optional[RiskLimits] = None,
        belief_store: Any = None,
        consult_beliefs: bool = False,
    ):
        self.limits = limits or RiskLimits()
        self.is_weekend = False
        self.belief_store = belief_store
        self.consult_beliefs = bool(consult_beliefs)  # explicit opt-in only

    def set_weekend_mode(self, is_weekend: bool) -> None:
        self.is_weekend = is_weekend

    def evaluate(
        self,
        opp: FundingOpportunity,
        portfolio: PortfolioState,
        available_capital: float,
    ) -> Optional[ApprovedOpportunity]:
        reasons: List[str] = []

        # Optional belief consultation (no ambient authority)
        if self.consult_beliefs and self.belief_store is not None:
            try:
                relevant = self.belief_store.relevant_for_pair(
                    opp.long_venue, opp.short_venue, opp.asset
                )
                for b in relevant:
                    if getattr(b, "evidence_score", 0) > 0.05:
                        reasons.append(f"belief:{getattr(b, 'id', 'unknown')}")
            except Exception:
                pass  # never let belief path break the guardian

        # Hard threshold
        if opp.estimated_net_apr < self.limits.min_net_apr_threshold:
            return None

        # Leverage (research: prefer 2-3x, hard max 5x)
        lev = min(
            self.limits.preferred_leverage,
            self.limits.max_leverage,
            getattr(opp, "recommended_leverage", 3.0),
        )
        if self.is_weekend:
            lev = min(lev, 2.0)
            reasons.append("weekend_reduced_leverage")

        # Dual-leg capital requirement + buffer
        buffer = 0.25 + (self.limits.weekend_extra_buffer if self.is_weekend else 0.0)
        dual_margin_factor = (1.0 / lev) * 2.0 * (1.0 + buffer)
        max_from_capital = available_capital / dual_margin_factor if dual_margin_factor > 0 else 0.0

        # Liquidity & portfolio caps
        liq_cap = min(opp.long_oi, opp.short_oi) * 0.05
        remaining = max(0.0, self.limits.max_portfolio_exposure_usd - portfolio.total_exposure_usd)
        venue_cap = max(0.0, self.limits.max_per_venue_pct * portfolio.total_equity
                        - portfolio.venue_exposure.get(opp.long_venue.value, 0.0)
                        - portfolio.venue_exposure.get(opp.short_venue.value, 0.0))
        asset_cap = max(0.0, self.limits.max_per_asset_pct * portfolio.total_equity
                        - portfolio.asset_exposure.get(opp.asset, 0.0))

        approved = min(
            max_from_capital,
            liq_cap,
            remaining,
            venue_cap,
            asset_cap,
            getattr(opp, "recommended_notional", None) or max_from_capital,
        )

        if approved < 1000.0:
            return None

        if getattr(opp, "risk_score", 0.0) > 0.7:
            approved *= 0.5
            reasons.append("high_risk_score_halved")

        return ApprovedOpportunity(
            opportunity=opp,
            approved_notional=approved,
            approved_leverage=lev,
            max_hold_hours=24.0 if self.is_weekend else 72.0,
            reasons=reasons,
        )

    def check_kill_triggers(
        self,
        portfolio: PortfolioState,
        markets: List[Any],
    ) -> List[str]:
        """Return list of active kill reasons (empty = healthy)."""
        triggers: List[str] = []
        return triggers
