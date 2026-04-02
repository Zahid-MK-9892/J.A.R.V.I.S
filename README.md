# Agentic Trading Bot (Starter Implementation)

This repository now includes a runnable starter implementation of an **agentic trading bot** with:
- Multi-agent flow (planner, news, risk).
- Strategy layer (swing momentum + intraday mean reversion).
- Paper broker execution.
- Config-driven runtime via `.env`.

> This is an educational engineering starter. It is **not** financial advice.

## What is implemented

- `agentic_trading_bot/data/providers.py`
  - Mock market/news data providers (safe offline default).
- `agentic_trading_bot/strategies/core.py`
  - Swing and intraday signal generation.
- `agentic_trading_bot/agents/`
  - Planner agent chooses best signal.
  - Risk agent sizes positions and approves/rejects trades.
- `agentic_trading_bot/brokers/paper.py`
  - In-memory paper broker with position/cash accounting.
- `agentic_trading_bot/execution/engine.py`
  - Orchestration loop (data -> strategy -> planner -> risk -> execution).
- `agentic_trading_bot/main.py`
  - CLI entrypoint.

---

## Step-by-step setup guide (non-tech friendly)

## Step 1) Install prerequisites

1. Install Python 3.11+.
2. Install Git.
3. Open terminal and clone repository.

```bash
git clone <your-repo-url>
cd web
```

## Step 2) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## Step 3) Install dependencies

```bash
pip install -e .
pip install -e .[dev]
```

## Step 4) Create environment file

Copy `.env.example` to `.env` and edit values.

```bash
cp .env.example .env
```

Minimum keys to change:
- `SYMBOLS` (example: `AAPL,MSFT,BTC-USD`)
- `STARTING_CASH`
- `RISK_PER_TRADE_PCT`

## Step 5) Run one cycle (quick test)

```bash
python -m agentic_trading_bot.main --once
```

You should see logs indicating either:
- no signal
- risk rejected
- paper order executed

## Step 6) Run continuously

```bash
python -m agentic_trading_bot.main
```

Stop with `Ctrl+C`.

## Step 7) Run tests

```bash
pytest -q
```

---

## Connecting real APIs next (incremental path)

1. Replace `MockMarketDataProvider` with real adapters (Alpaca/Polygon for stocks, Binance/Coinbase for crypto).
2. Replace `MockNewsProvider` with NewsAPI/Finnhub/Benzinga adapters.
3. Keep execution in paper mode until at least 4-8 weeks of stable results.
4. Add kill-switches before live mode.

---

## Current limitations

- Uses mock data by default (intentional for safety and quick setup).
- No live broker order routing in this starter commit.
- No historical backtest engine yet.

These are the next modules you should implement after paper-trading validation.
