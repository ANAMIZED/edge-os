# Edge OS

[![CI](https://github.com/ANAMIZED/edge-os/actions/workflows/ci.yml/badge.svg)](https://github.com/ANAMIZED/edge-os/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-server-purple.svg)](src/edge_os/mcp/)
[![SDK](https://img.shields.io/badge/SDK-Python-green.svg)](src/edge_os/sdk/)
[![CLI](https://img.shields.io/badge/CLI-edge--os-orange.svg)](src/edge_os/cli.py)
[![API](https://img.shields.io/badge/API-FastAPI-009688.svg)](src/edge_os/api/)

**Autonomous Agentic Operating System for RWA Perpetual Futures Arbitrage**

Edge OS continuously monitors, detects, sizes, and (in controlled modes) executes delta-neutral funding-rate, basis, and related strategies across Hyperliquid, Lighter, Binance, Ostium, Bybit, OKX and related venues.

**[Trading Decision Cycle ($4.00)](https://buy.stripe.com/bJedRaebsaLr2kZ2F243S05)** · **[Support Agentic OS Kernels ($99)](https://buy.stripe.com/bJecN63wObPv6Bf7Zm43S02)** · **[Public Goods Support](https://donate.stripe.com/00w5kE3wOg5L8Jn2F243S00)**

### Non-custodial USDC (preferred for agents)

| Network | Address | Explorer |
|---------|---------|----------|
| **Base** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [basescan](https://basescan.org/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Ethereum** | `0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438` | [etherscan](https://etherscan.io/address/0xD3d0E9eDAe3Ac7bb199a8EAA761BdA423b878438) |
| **Solana** | `ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A` | [solscan](https://solscan.io/account/ETQwWf19axArsY493UfC6bxe2BmEzmzvCb58PPnC38A) |

*Related:* [agenticarb](https://github.com/ANAMIZED/agenticarb) · [rui](https://github.com/ANAMIZED/rui) · [server-os](https://github.com/ANAMIZED/server-os) · [x402-cloudflare-starter](https://github.com/ANAMIZED/x402-cloudflare-starter)

## Surfaces

| Surface | Entry |
|---------|-------|
| **CLI** | `edge-os` / `python -m edge_os.cli` |
| **SDK** | `from edge_os.sdk import EdgeOSClient` |
| **REST API** | `edge-os-api` → http://localhost:8080/docs |
| **MCP Server** | `edge-os-mcp` |
| **Multi-agent workflows** | `edge_os.workflows` + `skills/multi-agent-workflow/` |
| **Verify** | `bash scripts/verify.sh` |
| **CI** | `.github/workflows/ci.yml` |

## Quick Start

```bash
pip install -e ".[dev,cli,api,mcp]"
bash scripts/verify.sh
edge-os-api   # REST on :8080
```

## Design principles

1. Fail closed (RiskGuardian, leverage hard caps, dual-leg buffers)
2. Research-aligned (preferred pairings, 2-5x, oracle gates, weekend buffers)
3. Offline/mock preferred for verification
4. Deployable with zero tribal knowledge
5. Multi-surface (SDK, CLI, MCP, API, Workflows, Skills)

## License

Apache-2.0
