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

if grep -qi "sealed-sandbox\|AQuA\|asymmetric" "$ROOT/AGENTS.md"; then
  green "AGENTS.md contains AQuA/sealed-sandbox governance"
else
  red "AGENTS.md missing AQuA governance language"
fi

for skill in discovery-distribution funding-arb aqua-research; do
  if [[ -f "$ROOT/skills/$skill/SKILL.md" ]]; then green "skill $skill present"; else red "skill $skill missing"; fi
done

info "Checking elite files..."
for f in LICENSE SECURITY.md CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md docs/DISCOVERY.md docs/SYNTHESIS.md; do
  if [[ -f "$ROOT/$f" ]]; then green "$f present"; else red "$f missing"; fi
done

if grep -qi "AQuA\|sealed\|belief" "$ROOT/docs/SYNTHESIS.md"; then
  green "SYNTHESIS.md contains AQuA alignment"
else
  red "SYNTHESIS.md missing AQuA language"
fi

info "Import all surfaces (offline)..."
if python -c "
from edge_os.models import Venue, RiskLimits, FundingOpportunity
from edge_os.risk.guardian import RiskGuardian, PortfolioState
from edge_os.detection.funding_spread import FundingSpreadDetector
from edge_os.sdk.client import EdgeOSClient
from edge_os.workflows.funding_arb import run_funding_arb_workflow
from edge_os.memory.beliefs import BeliefStore, ValidatedBelief
from edge_os.research.workflow import run_aqua_research_loop
from edge_os.research.evaluator import SealedEvaluator
print('imports ok')
"; then
  green "Kernel + SDK + Workflow + Memory + Research imports OK"
else
  red "Import failure"
fi

info "SDK + RiskGuardian smoke..."
if python -c "
from edge_os.sdk.client import EdgeOSClient
from edge_os.models import Venue, FundingOpportunity
c = EdgeOSClient()
opp = FundingOpportunity(
    asset='XAU', long_venue=Venue.LIGHTER, short_venue=Venue.HYPERLIQUID,
    long_funding_apr=0.05, short_funding_apr=0.25, gross_spread_apr=0.20,
    estimated_net_apr=0.15, long_oi=5e6, short_oi=5e6,
    liquidity_score=0.8, risk_score=0.3, recommended_leverage=3.0
)
approved = c.evaluate_risk(opp)
assert approved is not None and approved.approved_leverage <= 5.0
print('sdk risk ok')
"; then
  green "SDK + RiskGuardian smoke passed"
else
  red "SDK smoke failed"
fi

info "Multi-agent workflow smoke..."
if python -c "
from edge_os.workflows.funding_arb import run_funding_arb_workflow
r = run_funding_arb_workflow()
assert r['status'] == 'completed'
print('workflow ok')
"; then
  green "Funding-arb workflow passed"
else
  red "Workflow failed"
fi

info "AQuA Research Loop + BeliefStore smoke..."
if python -c "
from edge_os.research.workflow import run_aqua_research_loop
r = run_aqua_research_loop()
assert r['status'] == 'completed'
assert r.get('validated', 0) >= 1 or r.get('proposals', 0) >= 1
print('aqua research ok')
"; then
  green "AQuA Research Loop + BeliefStore passed"
else
  red "AQuA Research Loop failed"
fi

info "CLI import..."
if python -c "from edge_os.cli import app; print('cli ok')"; then
  green "CLI import OK"
else
  red "CLI import failed"
fi

info "MCP import..."
if python -c "from edge_os.mcp.server import mcp; print('mcp ok')"; then
  green "MCP import OK"
else
  red "MCP import failed"
fi

echo ""
echo "=============================="
echo " Edge OS verification result"
echo "=============================="
echo "  PASSED: $PASS"
echo "  FAILED: $FAIL"
echo "=============================="

if [[ "$FAIL" -eq 0 ]]; then
  echo "ALL CHECKS PASSED — AGENTS.md, skills, elite files, kernel, SDK, CLI, MCP, workflows, BeliefStore, AQuA Research Loop."
  exit 0
else
  echo "SOME CHECKS FAILED — inspect output above."
  exit 1
fi
