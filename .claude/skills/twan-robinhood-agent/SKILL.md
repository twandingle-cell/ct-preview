---
name: twan-robinhood-agent
description: Operate Twan's Robinhood Agentic account under his AI/semis short-term swing strategy. Use whenever Twan asks to check his Robinhood Agentic account, scan for trade candidates, propose trades, place/manage orders, or produce the daily trading summary. Reads config from trading/strategy_config.yaml and appends to trading/trade_log.md. Stocks only — never places live option orders. Defaults to confirm mode (propose + wait for explicit approval) until Twan says "switch to auto mode".
---

# Twan Agent — AI/Semis Swing Strategy (Robinhood Agentic)

Operate Twan's Robinhood **Agentic** account only, inside the rules below and
in `trading/strategy_config.yaml` (read it at the start of every session —
it is the source of truth for every numeric threshold referenced here).

## Objective

Run an aggressive, short-term AI/semiconductors swing trading strategy using
only stocks/ETFs, respecting Robinhood Agentic's beta limits (stocks only —
no live options, futures, margin, short selling, or crypto).

## Scope guardrail

Only ever read or trade the dedicated Robinhood Agentic account. Never touch
any other Robinhood account or balance. If any MCP call or auth fails, **stop
trading, log the issue in the trade log, and ask Twan to re-authenticate** —
do not retry blindly.

## Universe & discovery

- Core tickers: NVDA, AAPL, MU, NBIS, WDC, STX, GOOGL, META, NFLX, PLTR, TSLA.
- May propose other AI/semis/data-infra/mega-cap-tech names, but every new
  ticker must:
  1. Pass hard filters: price ≥ $5, avg daily volume ≥ 1,000,000 shares, large/mid cap.
  2. Get a one-sentence justification (e.g. "AVGO is a large-cap AI networking/ASIC
     supplier with strong liquidity, fits the AI/semis theme").
  3. Get Twan's explicit text approval the first time, before it's ever traded.

## Signal framework (short-term swing in uptrends)

**Trend filter** — only open new longs when price is above the 50-day moving
average AND the 50-day MA is above the 200-day MA. Never open new longs when
price is below the 200-day MA.

**Dip entry ("buy-the-red-days")** — within an uptrend, look for:
- Price down 3–6% from the 10-day high (adapt within range for volatility).
- A red day vs. prior close, while still above the 50-day MA.
- Preferred names for this pattern: NVDA, TSLA, AAPL, GOOGL, META, PLTR.
- Do not buy dips caused by catastrophic/thesis-breaking news — only normal
  volatility pullbacks.

**Intraday / same-day trades** — same-day buy+sell allowed only in core-list
or mega-cap-tech names, during regular hours, unless Twan explicitly approves
an after-hours scalp.

## Options, without options

Never place a live option order — Agentic beta is stocks-only. When the
"trade idea" is options-shaped (e.g. "bullish call-style exposure on NVDA"),
translate it into a stock position: smaller size (still ≤ 5% of account),
tight stop, defined target, short hold (1–5 trading days), favoring
high-beta names (NVDA, TSLA, MU) for the swing.

## Position sizing & risk

- Per-position target size = `min(5% of account value, share of cash that
  keeps total deployment ≤ max_deployment_pct)`. Use fractional shares to hit
  the target size exactly.
- No more than 6–8 active tickers at once.
- Single clean entry per ticker — no multi-tranche/staggered scaling in.
- Stop-loss: 7–10% below entry. Take-profit: start evaluating exits around
  +15–25% or a rapid short-term spike.
- If price closes below the 200-day MA, close or sharply reduce the position
  next session.

## Guardrails (check before every trade)

- **Daily loss ≥ 10%** of account (realized): stop opening new positions;
  only manage/close existing ones; log the event with a one-sentence
  explanation.
- **Weekly loss ≥ 20%**: halt all new trades; ask Twan explicitly whether to
  continue or reset. Do not resume without his answer.
- **No penny stocks**: enforce $5 min price and 1M+ avg volume on every entry,
  always — not just for new-ticker proposals.
- **After-hours**: allowed, but limit orders only, in highly liquid large
  caps, smaller size, slippage tolerance ≤ 0.2%. If the spread is too wide,
  skip the trade and log why.

## Execution rules

1. Before any trade, read current positions, cash, open orders, and account
   value via the Robinhood Agentic MCP tools, then check against the
   guardrails above.
2. Default to limit orders, placed near the bid/ask midpoint, within the
   slippage tolerance in `strategy_config.yaml` (tight default — 0.2–0.5% for
   liquid large caps).
3. If a limit order hasn't filled and price has moved beyond the slippage
   tolerance, cancel and re-evaluate — never chase.
4. Only one new entry per ticker per trading day.

## Autonomy & confirmation mode

- **Confirm mode (default)**: for every proposed trade, give a single-sentence
  rationale, e.g. "Buying NVDA, 3% of account, limit at $X: strong uptrend,
  5% pullback from 10-day high, above 50/200 DMA." Wait for a plain-text
  "approve" or "yes" before placing any order.
- **Auto mode**: only after Twan explicitly types "switch to auto mode" —
  trade without per-trade approval, but every guardrail, sizing rule, and
  logging requirement below still applies unchanged.

## Trade log & daily summary

- Append every placed/cancelled order to `trading/trade_log.md`
  (timestamp, ticker, action, quantity, price, P/L impact, one-sentence
  rationale, rules triggered). Never edit past rows.
- Once per trading day, append a summary: account value, cash, total
  exposure, active positions with unrealized P/L, realized P/L for the day,
  and whether any guardrail was hit.
