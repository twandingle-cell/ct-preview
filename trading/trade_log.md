# Trade Log — Twan Robinhood Agentic (AI/Semis Swing Strategy)

Persistent, append-only log of every order placed (or cancelled) under `trading/strategy_config.yaml`.
One row per event. Never edit past rows — append corrections as new rows.

| datetime | ticker | action | quantity | price | rationale | signal_type | risk_notes | result_after_exit |
|---|---|---|---|---|---|---|---|---|

## Daily Summaries

Appended once per trading day. Each entry: account value, cash, total exposure,
active positions with unrealized P/L, realized P/L for the day, and whether any
guardrail (daily/weekly loss stop) was hit.

<!-- Newest summary goes on top. -->
