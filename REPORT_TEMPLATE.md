# REPORT_TEMPLATE.md

Blueprint for the daily premarket report. This is the section skeleton only —
no live data here. The analyst and merge prompts (written later) fill in each
section using this as the structural contract.

**Voice:** Casual Humbled Trader voice. No em dashes.
**Conviction key:** 🟢 green / 🟡 yellow / 🔴 red (used consistently in every table).
**Process note:** Claude and Codex each run an independent pass. A rules engine
picks the watchlist candidates; both AIs judge setup quality on top of that —
neither AI is choosing which tickers make the list.

---

## 1. Title + Dated Subtitle

```
# [Report Title]
### [Day, Month D, YYYY] — Claude + Codex, independent passes
```

## 2. Disclaimer (one line)

```
Rules pick the watchlist. Both AIs judge quality. Not financial advice.
```

## 3. Summary

- **The tape in one line:** [one sentence on overall market tone/direction]
- **The catch we're watching:** [the single most important thing to watch today]
- **Two-brain verdict (one line):** [where Claude + Codex agree or disagree, condensed to one line]

## 4. Pre-Market Gappers

For each gapper, full catalyst headline (not just "earnings" — the actual news):

```
- **[TICKER]** [+/-X%] — [full catalyst headline]
- **[TICKER]** [+/-X%] — [full catalyst headline]
```

## 5. Day Trading Watchlist

| Ticker | Catalyst | Levels | Plan | Codex Check | Conviction |
|---|---|---|---|---|---|
| [TICK] | [catalyst] | [key levels] | [trade plan] | [Codex agrees/disagrees + why] | 🟢/🟡/🔴 |

## 6. Swing Watchlist

| Ticker | Catalyst | Trend Context | Idea | Codex Check | Conviction |
|---|---|---|---|---|---|
| [TICK] | [catalyst] | [trend context] | [swing idea] | [Codex agrees/disagrees + why] | 🟢/🟡/🔴 |

## 7. Market Trends of the Day

[Narrative on sector rotation, breadth, risk-on/risk-off, etc.]

## 8. Technical Signals for Today

[Key index levels, indicators, chart patterns worth flagging]

## 9. Economic Data, Rates and the Fed

[Pulled from the econ calendar — today's releases, Fed speakers, rate context]

## 10. Coming Up

[Tomorrow's econ events + earnings on deck]

## 11. Skips and Traps

[Setups that look tempting but the rules/AIs are passing on, and why]

## 12. Where the Two Brains Landed

- **Agreement:** [where Claude and Codex lined up]
- **Rules vs. discretion:** [where the rules engine and AI judgment diverged, if at all]
- **Claude's sharp catch:** [the one thing Claude flagged that stood out]
- **Codex's sharp catch:** [the one thing Codex flagged that stood out]
