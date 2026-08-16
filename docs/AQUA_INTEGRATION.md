# AQuA Integration Notes (Edge OS)

Based on arXiv:2608.12841 (AQuA: Recursively Self-Improving Quantitative Trading Research Agents).

## Adopted Patterns
- Sealed sandbox + asymmetric freedom
- Manager-mediated multi-agent research loop
- Evidence retention / BeliefStore
- Complete isolation between research and live/execution paths

## Surfaces
- `edge_os.research.run_aqua_research_loop`
- `edge_os.memory.BeliefStore`
- MCP tools: research_propose, research_evaluate, belief_update
- Skill: `skills/aqua-research`

## Governance
Research is optional, offline/paper by default, and never grants ambient authority over live capital.
