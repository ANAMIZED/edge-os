"""Belief / Evidence Memory — AQuA-inspired validated beliefs store.

Live FundingScanner and RiskGuardian may optionally consult this store.
Research Loop writes only validated evidence. Sealed from live capital path.
"""
from __future__ import annotations
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from edge_os.models import Venue


class ValidatedBelief(BaseModel):
    """A single piece of validated research evidence."""
    id: str
    hypothesis: str
    category: str  # funding_diff | oi_imbalance | weekend_gap | oracle_lag | ranking
    expression_or_config: str  # constrained symbolic form or ranking config
    evidence_score: float  # e.g. IC, net APR, hit rate on sealed eval
    venues: List[str] = Field(default_factory=list)
    assets: List[str] = Field(default_factory=list)
    validated_at: datetime = Field(default_factory=datetime.utcnow)
    holdout_metrics: Dict[str, float] = Field(default_factory=dict)
    notes: str = ""


class BeliefStore:
    """Persistent (in-memory for offline) store of validated beliefs."""

    def __init__(self) -> None:
        self._beliefs: Dict[str, ValidatedBelief] = {}

    def update(self, belief: ValidatedBelief) -> None:
        self._beliefs[belief.id] = belief

    def get(self, belief_id: str) -> Optional[ValidatedBelief]:
        return self._beliefs.get(belief_id)

    def list_by_category(self, category: str) -> List[ValidatedBelief]:
        return [b for b in self._beliefs.values() if b.category == category]

    def list_all(self) -> List[ValidatedBelief]:
        return list(self._beliefs.values())

    def relevant_for_pair(self, long_venue: Venue, short_venue: Venue, asset: str) -> List[ValidatedBelief]:
        """Optional consult for live scanner / guardian."""
        out = []
        for b in self._beliefs.values():
            if asset in b.assets or not b.assets:
                if long_venue.value in b.venues or short_venue.value in b.venues or not b.venues:
                    out.append(b)
        return out

    def dump(self) -> List[Dict[str, Any]]:
        return [b.model_dump(mode="json") for b in self._beliefs.values()]
