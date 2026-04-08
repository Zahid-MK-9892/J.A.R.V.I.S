from __future__ import annotations

from datetime import datetime, timezone
import random

from agentic_trading_bot.models import MarketSnapshot, NewsSignal


class MarketDataProvider:
    """Abstract market data provider."""

    def latest_price(self, symbol: str) -> MarketSnapshot:
        raise NotImplementedError


class NewsProvider:
    """Abstract news provider."""

    def sentiment(self, symbol: str) -> NewsSignal:
        raise NotImplementedError


class MockMarketDataProvider(MarketDataProvider):
    def __init__(self) -> None:
        self._state: dict[str, float] = {}

    def latest_price(self, symbol: str) -> MarketSnapshot:
        base = self._state.get(symbol, 100.0 if "BTC" not in symbol else 60_000.0)
        next_price = max(0.01, base * (1 + random.uniform(-0.005, 0.005)))
        self._state[symbol] = next_price
        return MarketSnapshot(
            symbol=symbol,
            price=round(next_price, 2),
            volume=random.uniform(1_000, 5_000_000),
            timestamp=datetime.now(timezone.utc),
        )


class MockNewsProvider(NewsProvider):
    def sentiment(self, symbol: str) -> NewsSignal:
        score = random.uniform(-1, 1)
        label = "positive" if score > 0.2 else "negative" if score < -0.2 else "neutral"
        return NewsSignal(
            symbol=symbol,
            sentiment=score,
            summary=f"Latest news sentiment for {symbol} looks {label}",
            timestamp=datetime.now(timezone.utc),
        )
