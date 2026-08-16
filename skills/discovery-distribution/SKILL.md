---
name: discovery-distribution
description: Run the discovery → synthesis → build → verify → elite-package → distribute loop to turn domain insight into a multi-surface, verified GitHub product. Use when productizing an idea, packaging agentic systems, or raising a repo to elite open-source standards before launch.
version: 0.1.0
license: Apache-2.0
tags: [discovery, distribution, productize, packaging, agents, skills, github, edge-os]
---

# Discovery & Distribution Skill (Edge OS)

## Process (six stages)

1. **Discovery** — demand, gaps, standards (see docs/DISCOVERY.md)
2. **Synthesis** — product identity, surfaces, acceptance contract (docs/SYNTHESIS.md)
3. **Build** — kernel then surfaces; every surface has an entrypoint
4. **Verify** — one script (`scripts/verify.sh`); stranger can run it; offline/mock preferred
5. **Elite package** — LICENSE, README, SECURITY, CONTRIBUTING, CoC, CHANGELOG, CI, templates
6. **Distribute** — public repo + install this skill into consumer trees

## Hard rules

- Fail closed on distribute: no public push without LICENSE + README + verify green
- Own repo is source of truth
- Prefer one acceptance command over tribal knowledge
- When building the package itself, dogfood: the repo must pass its own `scripts/verify.sh`
