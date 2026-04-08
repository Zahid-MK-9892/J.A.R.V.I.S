from __future__ import annotations

from agentic_trading_bot.models import MarketSnapshot, PortfolioState, RiskDecision, TradeSignal


class RiskAgent:
    def __init__(self, risk_per_trade_pct: float, max_position_pct: float) -> None:
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_position_pct = max_position_pct

    def review(self, signal: TradeSignal, snapshot: MarketSnapshot, portfolio: PortfolioState) -> RiskDecision:
        account_value = portfolio.cash
        for position in portfolio.positions.values():
            account_value += position.quantity * snapshot.price if position.symbol == snapshot.symbol else 0

        max_position_value = account_value * self.max_position_pct
        proposed_risk_value = account_value * self.risk_per_trade_pct * max(signal.confidence, 0.2)
        notional = min(max_position_value, proposed_risk_value)

        if notional < snapshot.price:
            return RiskDecision(False, 0.0, "position too small for current account size")

        quantity = round(notional / snapshot.price, 6)
        return RiskDecision(True, quantity, "risk checks passed")
