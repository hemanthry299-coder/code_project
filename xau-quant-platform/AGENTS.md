# XAU Quant Platform Engineering Rules

## Architecture

- Historical and live inputs may differ only in their adapters. Both must emit canonical market events and use the same candle, feature, strategy, risk, and execution interfaces.
- Use UTC internally. Convert time zones only in presentation code.
- Keep external-provider code isolated behind adapters and interfaces.
- Prefer small, typed, deterministic modules over speculative infrastructure.

## Market-data and research integrity

- Never use information unavailable at the timestamp under evaluation. In-progress higher-timeframe candles are never completed inputs.
- Historical replay must be event-by-event and must match the live pipeline after the adapter layer.
- Add and maintain automated historical/live parity tests for features, signals, entries, and exits.
- Never invent, fill, or hide missing data. Validate ordering, duplicates, OHLC consistency, gaps, volumes, reconnect recovery, and REST/WebSocket reconciliation.

## Trading safety

- This project is paper/shadow trading only. Do not add order-execution code, trading permissions, or automatic real-money trading.
- The deterministic risk engine owns account-risk decisions. LLM output is explanatory only and cannot override risk or place orders.
- Do not represent any strategy as profitable, guaranteed, or approved without recorded, out-of-sample evidence and configured validation gates.

## Strategy governance

- Every strategy has an immutable ID and semantic version. Never silently replace a version.
- Status transitions follow `RESEARCH -> VALIDATED -> APPROVED -> PAPER -> RETIRED`; approval requires documented validation gates.
- Model realistic spread, slippage, commission, funding, position limits, and trading-hour constraints in evaluation.

## Code, tests, and secrets

- Target Python 3.12+; type important public interfaces and use UTC-aware datetimes.
- Add focused pytest tests with meaningful components and run the relevant suite after every change.
- Store secrets only in `.env`; never commit, print, or log credentials or tokens. Keep `.env` ignored.
- Use structured logging without secrets. Update this file and architecture documentation when a material rule changes.
