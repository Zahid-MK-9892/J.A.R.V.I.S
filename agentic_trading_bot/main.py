from __future__ import annotations

import argparse
import logging

from agentic_trading_bot.brokers.paper import PaperBroker
from agentic_trading_bot.config import BotSettings
from agentic_trading_bot.data.providers import MockMarketDataProvider, MockNewsProvider
from agentic_trading_bot.execution.engine import TradingBot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the agentic trading bot starter")
    parser.add_argument("--once", action="store_true", help="Run one cycle only")
    return parser.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s | %(message)s")
    args = parse_args()
    settings = BotSettings()

    bot = TradingBot(
        settings=settings,
        market_data=MockMarketDataProvider(),
        news_provider=MockNewsProvider(),
        broker=PaperBroker(starting_cash=settings.starting_cash),
    )

    if args.once:
        bot.run_cycle()
        return

    bot.run_forever()


if __name__ == "__main__":
    main()
