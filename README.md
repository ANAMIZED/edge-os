# Edge OS

**Autonomous Agentic Operating System for RWA Perpetual Futures Arbitrage**

Edge OS is a multi-agent system designed to detect, evaluate, size, execute, and manage delta-neutral arbitrage strategies across centralized and decentralized exchanges offering perpetual futures on real-world assets (tokenized equities, commodities, forex, indices, pre-IPO).

Built on deep research into venues including Binance, Bybit, OKX, Hyperliquid (HIP-3), Lighter, Ostium, Kraken xStocks, and others.

## Core Strategies Supported
- Cross-venue Funding Rate / Rollover Arbitrage
- Weekend / Off-hours Basis & Gap Trading
- Cash-and-Carry (tokenized spot + perp)
- Price / Oracle Discrepancy Arbitrage
- Statistical / Relative Value (correlated RWAs)
- Pre-IPO / New Listing Flow

## Key Design Principles (from research)
- **Monitoring & Automation**: Continuous feeds from venue APIs + aggregators (Loris.tools, Coinglass, FundingView, Perps.com). Track premium vs index, OI imbalance, weekend gaps.
- **Leverage**: Strict max 2-5x for arb positions to survive gaps/ADL.
- **Preferred Venue Pairings**:
  - Lighter (zero-fee) + Hyperliquid / Binance
  - Ostium (stable real-carry rollover) + high-funding orderbook venues
  - Kraken xStocks (tokenized anchor) + synthetic perps
  - Binance (deep liquidity) + secondaries

## Architecture

### Agent Layer
- **Perception / Data Agents**: Normalize funding rates (1h vs 8h), prices, OI, oracle health across venues.
- **Opportunity Detection Agents**: FundingSpreadDetector, BasisGapDetector, etc.
- **RiskGuardian**: Position sizing, leverage limits, oracle anomaly detection (post-Ostium exploit awareness), gap buffers, portfolio correlation.
- **ExecutionBroker**: Multi-venue adapters (CEX via APIs, DEX via SDKs/web3), dry-run / live modes, simultaneous dual-leg entry.
- **Orchestrator / Supervisor**: Capital allocation, prioritization, human-in-loop / full-auto modes, kill switches.
- **Capital Mobility Agent**: Rebalancing USDT/USDC, bridges.

### Data & State
- Real-time + historical funding/premium stores
- Position and performance tracking
- Opportunity memory / learning

### Safety
- Hard risk limits from research
- Paper trading first
- Progressive capital deployment
- Audit logging

## Tech Stack
- Python 3.11+
- asyncio
- Pydantic for models
- ccxt / custom venue SDKs (Hyperliquid, Lighter, Ostium, etc.)
- Redis / Postgres for state
- FastAPI + dashboard (Streamlit/Gradio)
- Optional: LangGraph / CrewAI for higher-level agent orchestration

## Status
MVP in development: Funding rate scanner + paper trading on priority venues (Lighter, Hyperliquid, Binance).

## Team
Collaborative design by Grok (lead), Lucas (data/funding scanner), Benjamin (opportunity + risk), Harper (execution).

**Disclaimer**: Not financial advice. High risk of loss. Oracle, gap, liquidity, and counterparty risks are material. Always start in simulation.
