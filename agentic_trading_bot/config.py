from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    mode: str = Field(default="paper", description="paper or live")
    symbols: str = Field(default="AAPL,BTC-USD")
    poll_seconds: int = Field(default=60)

    starting_cash: float = Field(default=100_000.0)
    risk_per_trade_pct: float = Field(default=0.005)
    max_position_pct: float = Field(default=0.1)
    daily_loss_limit_pct: float = Field(default=0.03)

    alpha_vantage_api_key: str | None = None
    news_api_key: str | None = None

    @property
    def symbol_list(self) -> list[str]:
        return [s.strip().upper() for s in self.symbols.split(",") if s.strip()]
