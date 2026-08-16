---
name: aqua-research
description: AQuA-style recursive research loop for Edge OS. Offline/paper only. Manager proposes funding/OI/weekend/oracle hypotheses; specialists produce constrained expressions; sealed evaluator validates; beliefs written to BeliefStore for optional live consult.
version: 0.1.0
license: Apache-2.0
tags: [research, self-improvement, aqua, sealed-sandbox, beliefs]
---

# AQuA Research Skill (Edge OS)

## When to use
- Offline or paper mode only
- Improving detection / ranking logic over time
- Never coupled to live capital decisions without human gate

## Process
1. Manager proposes hypotheses (funding diffs, OI imbalance, weekend gaps, oracle lag)
2. Specialists convert to constrained expressions or ranking configs
3. SealedEvaluator (fixed splits, immutable metrics) scores on historical funding + mark/index
4. Validated beliefs → BeliefStore
5. Live FundingScanner / RiskGuardian may optionally consult BeliefStore

## Hard rules
- Sealed sandbox: agents cannot alter data, labels, or evaluator
- Fail closed: only validated evidence is retained
- Isolation: research path is separate from live execution path (AQuA asymmetry principle)
- Offline/mock preferred for verification
