from agentic_trading_bot.brokers.paper import PaperBroker
from agentic_trading_bot.models import Side


def test_paper_broker_buy_then_sell():
    broker = PaperBroker(starting_cash=10_000)

    buy = broker.place_order("AAPL", Side.BUY, quantity=10, price=100)
    assert buy.quantity == 10
    assert broker.portfolio.cash == 9000

    sell = broker.place_order("AAPL", Side.SELL, quantity=5, price=110)
    assert sell.quantity == 5
    assert broker.portfolio.cash == 9550
    assert broker.portfolio.positions["AAPL"].quantity == 5
