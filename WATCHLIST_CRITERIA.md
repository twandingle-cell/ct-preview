# WATCHLIST_CRITERIA.md

Source of truth for the two validated watchlist setups. The scanner encodes
these rules exactly. Nothing here is discretionary, this is what gets a
ticker on the list before any AI ever looks at it.

---

## Day Trading Watchlist: "Trend Join Long"

**Backtest:** 54.6% win rate, profit factor 1.59, 280 trades.

### Premarket selection (all required)

- Gap % vs prev close > 3%
- Price > $3
- Market cap > $1B
- Premarket relative volume (RVOL) > 1.5
- Price breaking above yesterday's high

### Intraday plan

- **Window:** 10:00am to 3:30pm ET
- **Trigger:** price > premarket high AND > prior high-of-day
- **Stop:** 1% below premarket high or LOD, whichever is lower = 1R
- **Scale:** 1/3 off at +1R, 1/3 off at +2R, trail the last 1/3 on the 21-EMA
- **Flat by:** 3:51pm

---

## Swing Watchlist

**Backtest:** 57.6% win rate / PF 5.34 on news catalysts. 44.7% win rate / PF 2.57 on earnings catalysts.

### Premarket selection (all required)

- Gap % >= 8%
- Price > $3
- Open > yesterday's high
- Open > 200-day SMA
- Market cap >= $800M
- A real catalyst (earnings on the gap day, or news with no earnings)

Swing entry and exit management is still being built. Swing entries on the
report are starter ideas only, no fake stops or targets.
