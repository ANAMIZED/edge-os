#!/usr/bin/env bash
# Edge OS end-to-end verification contract (offline/mock preferred).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PYTHONPATH="${ROOT}/src${PYTHONPATH:+:$PYTHONPATH}"
PASS=0
FAIL=0

green() { printf "\033[32m✓ %s\033[0m\n" "$*"; PASS=$((PASS+1)); }
red()   { printf "\033[31m✗ %s\033[0m\n" "$*"; FAIL=$((FAIL+1)); }
info()  { printf "\033[36m→ %s\033[0m\n" "$*"; }

info "Checking AGENTS.md and skills..."
if [[ -f "$ROOT/AGENTS.md" ]] && grep -q "verify.sh" "$ROOT/AGENTS.md"; then
  green "AGENTS.md present with verify contract"
else
  red "AGENTS.md missing or incomplete"
fi

if [[ -f "$ROOT/skills/discovery-distribution/SKILL.md" ]]; then
  green "discovery-distribution skill present"
else
  red "discovery-distribution skill missing"
fi

info "Checking elite files..."
for f in LICENSE SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md docs/DISCOVERY.md docs/SYNTHESIS.md; do
  if [[ -f "$ROOT/$f" ]]; then green "$f present"; else red "$f missing"; fi
done

info "Import kernel modules (offline)..."
if python -c "
from edge_os.models import Venue, RiskLimits, FundingOpportunity
from edge_os.risk.guardian import RiskGuardian, PortfolioState
from edge_os.detection.funding_spread import FundingSpreadDetector
print('imports ok')
"; then
  green "Kernel imports OK"
else
  red "Kernel import failure"
fi

info "RiskGuardian fail-closed smoke..."
if python -c "
from edge_os.models import Venue, FundingOpportunity, RiskLimits
from edge_os.risk.guardian import RiskGuardian, PortfolioState
from datetime import datetime
g = RiskGuardian(RiskLimits(min_net_apr_threshold=0.08))
opp = FundingOpportunity(
    asset='XAU', long_venue=Venue.LIGHTER, short_venue=Venue.HYPERLIQUID,
    long_funding_apr=0.05, short_funding_apr=0.25, gross_spread_apr=0.20,
    estimated_net_apr=0.15, long_oi=5e6, short_oi=5e6,
    liquidity_score=0.8, risk_score=0.3, recommended_leverage=3.0
)
port = PortfolioState(total_equity=100000.0)
approved = g.evaluate(opp, port, available_capital=50000.0)
assert approved is not None and approved.approved_leverage <= 5.0
print('risk ok')
"; then
  green "RiskGuardian smoke passed"
else
  red "RiskGuardian smoke failed"
fi

echo ""
echo "=============================="
echo " Edge OS verification result"
echo "=============================="
echo "  PASSED: $PASS"
echo "  FAILED: $FAIL"
echo "=============================="

if [[ "$FAIL" -eq 0 ]]; then
  echo "ALL CHECKS PASSED — AGENTS.md, skills, elite files, kernel, RiskGuardian."
  exit 0
else
  echo "SOME CHECKS FAILED — inspect output above."
  exit 1
fi
