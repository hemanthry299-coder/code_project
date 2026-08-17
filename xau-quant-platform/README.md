# XAU Quant Research & Live AI Analyst

Local, paper-only quantitative research and live market-analysis platform for Delta Exchange India gold-token perpetuals. It is deliberately not a trading bot: no real-money order execution is included or permitted.

## Status

Milestone 1 is scaffolded: repository skeleton, configuration, canonical typed models, and import tests are present. Test execution and Git initialization are blocked until Python 3.12+ and Git are installed. Downloading data, strategy logic, signals, and live connectivity are intentionally not implemented yet.

## Canonical architecture

```text
Delta REST historical adapter ─┐
                              ├─> canonical market events ─> candle engine ─> feature engine ─> strategy engine
Delta public WebSocket adapter ┘                                                               ├─> replay/backtest
                                                                                                └─> risk -> paper trading / alerts
```

Historical replay and live operation will share every component after their respective Delta adapters. UTC is the internal time standard; closed candles are the only strategy inputs.

## Instrument decision

On 18 August 2026, Delta India's public product catalogue lists the live gold-token perpetual `XAUTUSD` (Tether Gold Token, product ID `131253`) and `PAXGUSD`; it does not list an instrument literally named `XAUUSD`. The initial configuration uses `XAUTUSD`, but remains configurable because tokenized gold is not identical to a conventional spot XAUUSD feed.

## Delta API references verified

- REST base: `https://api.india.delta.exchange`; public historical candles: `GET /v2/history/candles`.
- Historical candle inputs are `resolution`, `symbol`, `start`, and `end` (Unix seconds); the response ceiling is 2,000 candles. The public endpoint needs no authentication.
- Public WebSocket: `wss://public-socket.india.delta.exchange`; use current public channel names such as `candlestick_1m`, `trades`, `ob_l2`, and `ticker`, rather than legacy private-endpoint channels. Candle messages document `o`, `h`, `l`, `c`, `v`, `res`, `sy`, `ts`, and `type`.
- The public WebSocket requires activity within 60 seconds and limits connection attempts to 150 per IP per five minutes.

Source: [Delta Exchange API documentation](https://docs.delta.exchange/).

## Layout

- `src/`: implementation packages, separated by data adapter, market pipeline, features, strategy, backtest, live, AI, alerts, and common types.
- `config/`: non-secret instrument, strategy, and environment configuration.
- `data/`: ignored local Parquet/DuckDB storage partitions.
- `tests/`: unit, integration, data-quality, and strategy tests.

## Setup (after Python and Git are installed)

```powershell
cd C:\Users\hemanth\Desktop\project_trail\xau-quant-platform
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
```

Install optional capability sets only when their milestones start, e.g. `.[dev,research,dashboard,ai]`.

## Safety rules

Read [AGENTS.md](AGENTS.md) before making changes. It defines the no-look-ahead, live/historical parity, data-quality, strategy-versioning, secret-management, and no-automatic-trading rules.
