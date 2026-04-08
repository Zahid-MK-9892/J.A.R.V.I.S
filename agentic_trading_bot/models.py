from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Side(str, Enum):
    BUY = "buy"
    SELL = "sell"


@dataclass(slots=True)
class MarketSnapshot:
    symbol: str
    price: float
    timestamp: datetime
    volume: float | None = None


@dataclass(slots=True)
class NewsSignal:
    symbol: str
    sentiment: float
    summary: str
    timestamp: datetime


@dataclass(slots=True)
class TradeSignal:
    symbol: str
    side: Side
    confidence: float
    reason: str


@dataclass(slots=True)
class RiskDecision:
    approved: bool
    quantity: float = 0.0
    reason: str = ""


@dataclass(slots=True)
class Order:
    symbol: str
    side: Side
    quantity: float
    price: float
    timestamp: datetime


@dataclass(slots=True)
class Position:
    symbol: str
    quantity: float = 0.0
    avg_price: float = 0.0


@dataclass(slots=True)
class PortfolioState:
    cash: float
    positions: dict[str, Position] = field(default_factory=dict)
