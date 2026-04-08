from agentic_trading_bot.agents.risk import RiskAgent
from agentic_trading_bot.models import MarketSnapshot, PortfolioState, Side, TradeSignal
from datetime import datetime, timezone


def test_risk_agent_approves_with_quantity():
    agent = RiskAgent(risk_per_trade_pct=0.01, max_position_pct=0.1)
    signal = TradeSignal(symbol="AAPL", side=Side.BUY, confidence=0.5, reason="test")
    snapshot = MarketSnapshot(symbol="AAPL", price=100.0, volume=1000, timestamp=datetime.now(timezone.utc))
    portfolio = PortfolioState(cash=100_000)

    decision = agent.review(signal, snapshot, portfolio)

    assert decision.approved is True
    assert decision.quantity > 0
