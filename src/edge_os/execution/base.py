"""
Edge OS Execution Layer
Abstract brokers, dry-run simulator, multi-venue manager.
Aligned with RWA arb research: 2-5x lev, Lighter zero-fee priority, Ostium rollover, gap buffers, oracle risk.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum
import uuid
import asyncio
# from edge_os.models import Venue, Opportunity  # shared

class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"

class OrderRequest(BaseModel):
    venue: str  # Venue
    symbol: str
    side: OrderSide
    size_usd: float
    order_type: OrderType = OrderType.MARKET
    price: Optional[float] = None
    leverage: float = 3.0
    reduce_only: bool = False
    client_order_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

class Fill(BaseModel):
    order_id: str
    venue: str
    symbol: str
    side: OrderSide
    size_usd: float
    price: float
    fee: float
    timestamp: datetime

class Position(BaseModel):
    venue: str
    symbol: str
    size: float
    entry_price: float
    current_price: float
    unrealized_pnl: float
    margin_used: float
    leverage: float
    accrued_funding: float = 0.0
    opened_at: datetime

class ExecutionResult(BaseModel):
    success: bool
    opportunity_id: str
    fills: List[Fill] = []
    positions: List[Position] = []
    error: Optional[str] = None
    mode: str = "paper"

class ExecutionBroker(ABC):
    @abstractmethod
    async def place_order(self, req: OrderRequest) -> Fill:
        pass
    @abstractmethod
    async def get_positions(self) -> List[Position]:
        pass
    @abstractmethod
    async def get_balance(self, asset: str = "USDC") -> float:
        pass
    @abstractmethod
    async def close_position(self, venue: str, symbol: str, size: Optional[float] = None) -> Fill:
        pass

class DryRunBroker(ExecutionBroker):
    """Paper simulator with research-based fees, funding accrual, slippage."""
    def __init__(self, initial_balances: Dict[str, float] = None):
        self.balances = initial_balances or {"USDC": 100000.0, "USDT": 100000.0}
        self.positions: Dict[str, Position] = {}
        self.fills_history: List[Fill] = []
        self.fee_table = {
            "lighter": {"maker": 0.0, "taker": 0.0},
            "hyperliquid": {"maker": 0.0003, "taker": 0.0009},
            "binance": {"maker": 0.0002, "taker": 0.0004},
            "ostium": {"open": 0.0004, "close": 0.0},
        }
    async def place_order(self, req: OrderRequest) -> Fill:
        fee_rate = self.fee_table.get(req.venue, {"taker": 0.0005}).get("taker", 0.0005)
        fee = req.size_usd * fee_rate
        fill_price = req.price or 100.0
        fill = Fill(
            order_id=str(uuid.uuid4()),
            venue=req.venue,
            symbol=req.symbol,
            side=req.side,
            size_usd=req.size_usd,
            price=fill_price,
            fee=fee,
            timestamp=datetime.now(timezone.utc)
        )
        self.fills_history.append(fill)
        # TODO: full position update + funding accrual simulation
        return fill
    async def get_positions(self) -> List[Position]:
        return list(self.positions.values())
    async def get_balance(self, asset: str = "USDC") -> float:
        return self.balances.get(asset, 0.0)
    async def close_position(self, venue: str, symbol: str, size: Optional[float] = None) -> Fill:
        pass  # implement

class MultiVenueManager:
    def __init__(self, brokers: Dict[str, ExecutionBroker] = None):
        self.brokers = brokers or {}
        self.dry_run = DryRunBroker()
    async def execute_opportunity(self, opp: Any, mode: str = "paper") -> ExecutionResult:
        broker = self.dry_run if mode == "paper" else self.brokers.get(opp.long_venue)
        # Dual leg concurrent placement
        long_req = OrderRequest(venue=opp.long_venue, symbol=opp.asset, side=OrderSide.BUY, size_usd=opp.suggested_size_usd, leverage=3.0)
        short_req = OrderRequest(venue=opp.short_venue, symbol=opp.asset, side=OrderSide.SELL, size_usd=opp.suggested_size_usd, leverage=3.0)
        long_fill, short_fill = await asyncio.gather(
            broker.place_order(long_req),
            broker.place_order(short_req)
        )
        return ExecutionResult(success=True, opportunity_id=getattr(opp, 'id', 'unknown'), fills=[long_fill, short_fill], mode=mode)
