"""Sealed Evaluator — fixed data splits, immutable metrics. Offline mock."""
from __future__ import annotations
from typing import Dict, Any, List
from edge_os.memory.beliefs import ValidatedBelief
import hashlib
from datetime import datetime


class SealedEvaluator:
    """Fixed splits + metrics. Agents cannot alter data or labels."""

    def __init__(self) -> None:
        # Mock historical stats (offline)
        self.fixed_universe = ["XAU", "XAG", "NVDA", "TSLA", "CL"]
        self.fixed_splits = {"train": 0.6, "val": 0.2, "holdout": 0.2}

    def evaluate_expression(self, hypothesis: str, expression: str, category: str) -> Dict[str, Any]:
        """Return sealed metrics. Deterministic mock based on hash for offline verify."""
        h = int(hashlib.md5((hypothesis + expression).encode()).hexdigest()[:8], 16)
        score = 0.05 + (h % 200) / 1000.0  # 0.05 – 0.25 range
        return {
            "ic": round(score, 4),
            "net_apr_proxy": round(score * 1.8, 4),
            "hit_rate": round(0.5 + score, 3),
            "holdout_sharpe_proxy": round(score * 8, 2),
            "split": "holdout",
            "sealed": True,
        }

    def promote_if_valid(self, hypothesis: str, expression: str, category: str, threshold: float = 0.08) -> ValidatedBelief | None:
        metrics = self.evaluate_expression(hypothesis, expression, category)
        if metrics["net_apr_proxy"] >= threshold:
            bid = hashlib.md5((hypothesis + expression).encode()).hexdigest()[:12]
            return ValidatedBelief(
                id=bid,
                hypothesis=hypothesis,
                category=category,
                expression_or_config=expression,
                evidence_score=metrics["net_apr_proxy"],
                holdout_metrics=metrics,
                validated_at=datetime.utcnow(),
                notes="sealed_eval_pass",
            )
        return None
