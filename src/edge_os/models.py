from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class Venue(str, Enum):
    HYPERLIQUID = "hyperliquid"
    BINANCE = "binance"
    BYBIT = "bybit"
    OKX = "okx"
    LIGHTER = "lighter"
    OSTIUM = "ostium"
    KRACKEN = "kraken"
    EDGE_X = "edgex"
    ASTER = "aster"
    GRVT = "grvt"
    APEX = "apex"
    PACIFICA = "pacifica"
    AVANTIS = "avantis"
    EXTENDED = "extended"
    # Add others as needed

class AssetClass(str, Enum):
    COMMODITY = "commodity"
    EQUITY = "equity"
    INDEX = "index"
    FOREX = "forex"
    PRE_IPO = "pre_ipo"
    ETF = "etf"
    CRYPTO = "crypto"

class NormalizedMarket(BaseModel):
    """Normalized view of a RWA perp market across venues."""
    venue: Venue
    symbol: str  # e.g. "XAU-USDC", "NVDA-USDT"
    base_asset: str  # "XAU", "NVDA"
    asset_class: AssetClass
    mark_price: float
    index_price: Optional[float] = None
    funding_rate: float  # raw rate for the interval
    funding_interval_hours: float  # 1.0 or 8.0 typically
    funding_apr: float  # annualized for comparison
    open_interest: float  # USD
    volume_24h: Optional[float] = None
    max_leverage: float = 20.0
    maker_fee: float = 0.0002
    taker_fee: float = 0.0005
    oracle_source: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    extra: Dict[str, Any] = Field(default_factory=dict)

class FundingOpportunity(BaseModel):
    """Detected funding rate arbitrage opportunity."""
    asset: str
    long_venue: Venue
    short_venue: Venue
    long_funding_apr: float
    short_funding_apr: float
    gross_spread_apr: float
    estimated_net_apr: float  # after fees
    long_oi: float
    short_oi: float
    liquidity_score: float  # 0-1
    risk_score: float  # 0-1 higher = riskier (oracle, gap, etc.)
    recommended_leverage: float = 3.0
    recommended_notional: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: str = ""

class Position(BaseModel):
    venue: Venue
    symbol: str
    side: str  # "long" or "short"
    size: float  # signed or absolute + side
    entry_price: float
    current_price: float
    unrealized_pnl: float = 0.0
    margin_used: float = 0.0
    leverage: float = 1.0
    funding_accrued: float = 0.0
    opened_at: datetime = Field(default_factory=datetime.utcnow)

class RiskLimits(BaseModel):
    max_leverage: float = 5.0
    preferred_leverage: float = 3.0
    max_portfolio_exposure_usd: float = 100000.0
    max_per_venue_pct: float = 0.4
    max_per_asset_pct: float = 0.2
    min_net_apr_threshold: float = 0.08  # 8% after costs
    oracle_deviation_bps_threshold: float = 50.0
    weekend_extra_buffer: float = 0.3  # 30% extra margin Fri-Sun
