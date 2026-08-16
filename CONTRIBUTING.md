# Contributing to Edge OS

## The contract

1. `bash scripts/verify.sh` must pass
2. Risk remains fail-closed
3. Research-aligned pairings and limits stay intact
4. Mock/offline path stays deterministic

Read `AGENTS.md` before changing code.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
bash scripts/verify.sh
```

## PRs

- Small, focused changes
- Describe why / what / how verified
- Update README, AGENTS.md, or skills when public surfaces change
