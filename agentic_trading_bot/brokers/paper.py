from __future__ import annotations

from datetime import datetime, timezone

from agentic_trading_bot.models import Order, PortfolioState, Position, Side


class PaperBroker:
    def __init__(self, starting_cash: float) -> None:
        self.portfolio = PortfolioState(cash=starting_cash)
        self.orders: list[Order] = []

    def place_order(self, symbol: str, side: Side, quantity: float, price: float) -> Order:
        position = self.portfolio.positions.get(symbol, Position(symbol=symbol))
        notional = quantity * price

        if side == Side.BUY:
            if self.portfolio.cash < notional:
                raise ValueError("Insufficient cash in paper account")
            new_qty = position.quantity + quantity
            position.avg_price = ((position.avg_price * position.quantity) + notional) / new_qty if new_qty else 0.0
            position.quantity = new_qty
            self.portfolio.cash -= notional
        else:
            if position.quantity < quantity:
                raise ValueError("Cannot sell more than current position in paper account")
            position.quantity -= quantity
            self.portfolio.cash += notional
            if position.quantity == 0:
                position.avg_price = 0.0

        self.portfolio.positions[symbol] = position
        order = Order(symbol=symbol, side=side, quantity=quantity, price=price, timestamp=datetime.now(timezone.utc))
        self.orders.append(order)
        return order
