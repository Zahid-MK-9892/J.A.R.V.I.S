from __future__ import annotations

from collections import defaultdict, deque

from agentic_trading_bot.models import MarketSnapshot, NewsSignal, Side, TradeSignal


class SwingMomentumStrategy:
    """Simple moving-average crossover style signal."""

    def __init__(self, short_window: int = 5, long_window: int = 20) -> None:
        self.short_window = short_window
        self.long_window = long_window
        self.history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=long_window))

    def evaluate(self, snapshot: MarketSnapshot) -> TradeSignal | None:
        prices = self.history[snapshot.symbol]
        prices.append(snapshot.price)
        if len(prices) < self.long_window:
            return None

        short_ma = sum(list(prices)[-self.short_window:]) / self.short_window
        long_ma = sum(prices) / len(prices)
        delta = (short_ma - long_ma) / long_ma

        if delta > 0.002:
            return TradeSignal(snapshot.symbol, Side.BUY, min(1.0, abs(delta) * 100), "swing momentum uptrend")
        if delta < -0.002:
            return TradeSignal(snapshot.symbol, Side.SELL, min(1.0, abs(delta) * 100), "swing momentum downtrend")
        return None


class IntradayMeanReversionStrategy:
    def __init__(self, lookback: int = 10) -> None:
        self.lookback = lookback
        self.history: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=lookback))

    def evaluate(self, snapshot: MarketSnapshot, news: NewsSignal) -> TradeSignal | None:
        prices = self.history[snapshot.symbol]
        prices.append(snapshot.price)
        if len(prices) < self.lookback:
            return None

        average = sum(prices) / len(prices)
        deviation = (snapshot.price - average) / average
        sentiment_boost = news.sentiment * 0.002

        if deviation < -0.004 and sentiment_boost >= 0:
            confidence = min(1.0, abs(deviation) * 100)
            return TradeSignal(snapshot.symbol, Side.BUY, confidence, "intraday mean reversion long")

        if deviation > 0.004 and sentiment_boost <= 0:
            confidence = min(1.0, abs(deviation) * 100)
            return TradeSignal(snapshot.symbol, Side.SELL, confidence, "intraday mean reversion short")
        return None
