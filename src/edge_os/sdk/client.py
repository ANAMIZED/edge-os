"""Edge OS Python SDK — offline-capable client for opportunities, risk, portfolio."""
from __future__ import annotations
from typing import Any, List, Optional
from edge_os.models import NormalizedMarket, FundingOpportunity, RiskLimits, Venue
from edge_os.risk.guardian import RiskGuardian, PortfolioState, ApprovedOpportunity
from edge_os.detection.funding_spread import FundingSpreadDetector

class EdgeOSClient:
    """Synchronous client for Edge OS kernel (offline by default)."""

    def __init__(self, limits: Optional[RiskLimits] = None) -> None:
        self.guardian = RiskGuardian(limits or RiskLimits())
        self.detector = FundingSpreadDetector()

    def detect_opportunities(self, markets: List[NormalizedMarket]) -> List[FundingOpportunity]:
        return self.detector.detect(markets)

    def evaluate_risk(
        self,
        opp: FundingOpportunity,
        portfolio: Optional[PortfolioState] = None,
        available_capital: float = 50_000.0,
    ) -> Optional[ApprovedOpportunity]:
        port = portfolio or PortfolioState(total_equity=available_capital)
        return self.guardian.evaluate(opp, port, available_capital)

    def health(self) -> dict[str, Any]:
        return {"status": "ok", "surfaces": ["sdk", "risk", "detection"]}
