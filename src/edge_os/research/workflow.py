"""AQuA-style Research Loop — offline / paper only.

Manager proposes hypotheses → Specialists produce constrained expressions
→ SealedEvaluator → BeliefStore update.
"""
from __future__ import annotations
from typing import List, Dict, Any
from edge_os.memory.beliefs import BeliefStore, ValidatedBelief
from edge_os.research.evaluator import SealedEvaluator


def _manager_propose() -> List[Dict[str, str]]:
    """Manager agent: propose research hypotheses (offline fixed set for verify)."""
    return [
        {"hypothesis": "Funding differential between Lighter and Hyperliquid widens on weekends", "category": "weekend_gap"},
        {"hypothesis": "OI imbalance > 2:1 predicts short-term funding mean-reversion", "category": "oi_imbalance"},
        {"hypothesis": "Oracle lag > 30s on Ostium increases basis risk", "category": "oracle_lag"},
        {"hypothesis": "XAU funding APR spread Lighter-Binance persists after fees", "category": "funding_diff"},
    ]


def _specialist_convert(hyp: Dict[str, str]) -> str:
    """Specialist: turn hypothesis into constrained expression / ranking config."""
    cat = hyp["category"]
    if cat == "weekend_gap":
        return "if is_weekend and abs(funding_apr[LIGHTER]-funding_apr[HYPERLIQUID]) > 0.05: boost_score 1.2"
    if cat == "oi_imbalance":
        return "oi_ratio = oi[long]/oi[short]; if oi_ratio > 2 or oi_ratio < 0.5: adjust_risk 0.7"
    if cat == "oracle_lag":
        return "if oracle_delay_s > 30: risk_score += 0.3; reject if > 0.8"
    return "net_apr = short_apr - long_apr - fees; rank by net_apr desc"


def run_aqua_research_loop(store: BeliefStore | None = None) -> Dict[str, Any]:
    """Full offline research loop. Returns summary + any newly validated beliefs."""
    store = store or BeliefStore()
    evaluator = SealedEvaluator()
    proposals = _manager_propose()
    validated: List[ValidatedBelief] = []

    for hyp in proposals:
        expr = _specialist_convert(hyp)
        belief = evaluator.promote_if_valid(hyp["hypothesis"], expr, hyp["category"])
        if belief:
            # Attach illustrative venues/assets
            belief.venues = ["lighter", "hyperliquid", "binance", "ostium"]
            belief.assets = ["XAU", "XAG"]
            store.update(belief)
            validated.append(belief)

    return {
        "workflow": "aqua_research_loop",
        "proposals": len(proposals),
        "validated": len(validated),
        "beliefs": [b.model_dump(mode="json") for b in validated],
        "status": "completed",
        "sealed": True,
    }
