"""Foundation imports must work without network access or credentials."""

from datetime import UTC, datetime

from common.types import Candle, StrategyStatus, StrategyVersion, Timeframe
from market.events import MarketTick


def test_canonical_models_import_and_construct() -> None:
    timestamp = datetime(2026, 8, 18, 9, 30, tzinfo=UTC)
    tick = MarketTick(timestamp=timestamp, symbol="XAUTUSD", price=4357.2, source="test")
    candle = Candle(
        timestamp=timestamp,
        symbol="XAUTUSD",
        timeframe=Timeframe.ONE_MINUTE,
        open=4350.0,
        high=4360.0,
        low=4348.0,
        close=4357.2,
        volume=12.5,
        source="test",
        is_closed=True,
    )
    version = StrategyVersion(
        strategy_id="LIQUIDITY_BOS",
        version="0.1.0",
        description="Registry-model import test only.",
        status=StrategyStatus.RESEARCH,
        created_at=timestamp,
    )

    assert tick.price == candle.close
    assert version.status is StrategyStatus.RESEARCH
