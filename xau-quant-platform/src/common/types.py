"""Canonical typed models shared by historical replay and live analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping


class Timeframe(StrEnum):
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"


class SignalDirection(StrEnum):
    LONG = "LONG"
    SHORT = "SHORT"
    FLAT = "FLAT"


class StrategyStatus(StrEnum):
    RESEARCH = "RESEARCH"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    PAPER = "PAPER"
    RETIRED = "RETIRED"


def _require_utc(timestamp: datetime) -> None:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware UTC instants")


@dataclass(frozen=True, slots=True)
class MarketTick:
    timestamp: datetime
    symbol: str
    price: float
    source: str
    volume: float | None = None

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)
        if self.price <= 0:
            raise ValueError("price must be positive")


@dataclass(frozen=True, slots=True)
class TradeEvent:
    timestamp: datetime
    symbol: str
    price: float
    size: float
    side: SignalDirection
    source: str

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)
        if self.price <= 0 or self.size <= 0:
            raise ValueError("trade price and size must be positive")


@dataclass(frozen=True, slots=True)
class OrderBookEvent:
    timestamp: datetime
    symbol: str
    bids: tuple[tuple[float, float], ...]
    asks: tuple[tuple[float, float], ...]
    source: str
    sequence: int | None = None

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)


@dataclass(frozen=True, slots=True)
class Candle:
    timestamp: datetime
    symbol: str
    timeframe: Timeframe
    open: float
    high: float
    low: float
    close: float
    volume: float
    source: str
    is_closed: bool

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)
        if min(self.open, self.high, self.low, self.close) <= 0:
            raise ValueError("OHLC prices must be positive")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("invalid OHLC range")
        if self.volume < 0:
            raise ValueError("candle volume cannot be negative")


@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    timestamp: datetime
    symbol: str
    timeframe: Timeframe
    values: Mapping[str, Any]

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)


@dataclass(frozen=True, slots=True)
class MarketState:
    timestamp: datetime
    symbol: str
    price: float
    candles: Mapping[Timeframe, Candle]
    features: Mapping[Timeframe, FeatureSnapshot]
    data_is_healthy: bool
    unresolved_gap_count: int = 0

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)
        if self.price <= 0 or self.unresolved_gap_count < 0:
            raise ValueError("market state contains invalid price or gap count")


@dataclass(frozen=True, slots=True)
class StrategySignal:
    timestamp: datetime
    strategy_id: str
    strategy_version: str
    symbol: str
    direction: SignalDirection
    state: str
    entry_price: float | None = None
    stop_loss: float | None = None
    take_profit: float | None = None
    rationale: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)


@dataclass(frozen=True, slots=True)
class RiskDecision:
    timestamp: datetime
    allowed: bool
    reason: str
    risk_amount: float | None = None
    position_size: float | None = None

    def __post_init__(self) -> None:
        _require_utc(self.timestamp)


@dataclass(frozen=True, slots=True)
class PaperTrade:
    trade_id: str
    signal_timestamp: datetime
    strategy_id: str
    strategy_version: str
    symbol: str
    direction: SignalDirection
    entry_price: float
    stop_loss: float
    take_profit: float
    simulated_fill_price: float | None = None
    exit_price: float | None = None
    outcome: str | None = None

    def __post_init__(self) -> None:
        _require_utc(self.signal_timestamp)


@dataclass(frozen=True, slots=True)
class StrategyVersion:
    strategy_id: str
    version: str
    description: str
    status: StrategyStatus
    created_at: datetime
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_utc(self.created_at)
