# Detailed Implementation Setup Guide

This guide explains how to run and extend the code in this repository.

## 1. Clone and install

```bash
git clone <repo-url>
cd web
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -e .[dev]
```

## 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:
- `SYMBOLS=AAPL,MSFT,BTC-USD`
- `STARTING_CASH=100000`
- `RISK_PER_TRADE_PCT=0.005`
- `MAX_POSITION_PCT=0.1`

## 3. Smoke test

```bash
python -m agentic_trading_bot.main --once
```

## 4. Continuous run (paper mode)

```bash
python -m agentic_trading_bot.main
```

## 5. Run test suite

```bash
pytest -q
```

## 6. Integrate real market APIs (next step)

1. Create new provider classes under `agentic_trading_bot/data/`.
2. Implement `latest_price(symbol)` from stock/crypto APIs.
3. Wire providers in `agentic_trading_bot/main.py`.
4. Keep paper broker enabled.

## 7. Integrate real news APIs (next step)

1. Implement news adapter returning `NewsSignal`.
2. Replace `MockNewsProvider` in `main.py`.
3. Add caching and retry logic.

## 8. Add production safety before live mode

- Daily loss kill switch.
- Circuit breaker for API/data outages.
- Audit log storage.
- Manual approval toggle before order submit.

## 9. Live mode checklist

- [ ] 4-8 weeks paper trading complete.
- [ ] Drawdown within limits.
- [ ] Monitoring and alerts active.
- [ ] Incident runbook prepared.
- [ ] Start with very small capital.
