from __future__ import annotations

import logging
import time

from agentic_trading_bot.agents.research import NewsAgent, PlannerAgent
from agentic_trading_bot.agents.risk import RiskAgent
from agentic_trading_bot.brokers.paper import PaperBroker
from agentic_trading_bot.config import BotSettings
from agentic_trading_bot.data.providers import MarketDataProvider, NewsProvider
from agentic_trading_bot.strategies.core import IntradayMeanReversionStrategy, SwingMomentumStrategy

logger = logging.getLogger(__name__)


class TradingBot:
    def __init__(
        self,
        settings: BotSettings,
        market_data: MarketDataProvider,
        news_provider: NewsProvider,
        broker: PaperBroker,
    ) -> None:
        self.settings = settings
        self.market_data = market_data
        self.news_provider = news_provider
        self.broker = broker

        self.swing = SwingMomentumStrategy()
        self.intraday = IntradayMeanReversionStrategy()
        self.news_agent = NewsAgent()
        self.planner = PlannerAgent()
        self.risk = RiskAgent(settings.risk_per_trade_pct, settings.max_position_pct)

    def run_cycle(self) -> None:
        for symbol in self.settings.symbol_list:
            snapshot = self.market_data.latest_price(symbol)
            news = self.news_provider.sentiment(symbol)

            candidates = [
                self.swing.evaluate(snapshot),
                self.intraday.evaluate(snapshot, news),
            ]
            selected = self.planner.pick(candidates)
            if not selected:
                logger.info("%s: no trade signal", symbol)
                continue

            risk = self.risk.review(selected, snapshot, self.broker.portfolio)
            if not risk.approved:
                logger.info("%s: risk rejected signal (%s)", symbol, risk.reason)
                continue

            try:
                order = self.broker.place_order(symbol, selected.side, risk.quantity, snapshot.price)
                logger.info(
                    "%s %s qty=%s @ %s | reason=%s | news=%s",
                    order.side.value.upper(),
                    order.symbol,
                    order.quantity,
                    order.price,
                    selected.reason,
                    self.news_agent.summarize(news),
                )
            except ValueError as exc:
                logger.warning("%s: order rejected: %s", symbol, exc)

    def run_forever(self) -> None:
        logger.info("Starting bot in %s mode for symbols=%s", self.settings.mode, self.settings.symbol_list)
        while True:
            self.run_cycle()
            time.sleep(self.settings.poll_seconds)
