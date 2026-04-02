from __future__ import annotations

from agentic_trading_bot.models import NewsSignal, TradeSignal


class NewsAgent:
    def summarize(self, signal: NewsSignal) -> str:
        polarity = "bullish" if signal.sentiment > 0.2 else "bearish" if signal.sentiment < -0.2 else "neutral"
        return f"{signal.summary}. Classified as {polarity}."


class PlannerAgent:
    """Chooses between signals and keeps only confident ideas."""

    def pick(self, candidates: list[TradeSignal | None]) -> TradeSignal | None:
        valid = [c for c in candidates if c is not None and c.confidence >= 0.2]
        if not valid:
            return None
        return sorted(valid, key=lambda s: s.confidence, reverse=True)[0]
