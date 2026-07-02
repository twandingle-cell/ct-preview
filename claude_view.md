# Premarket Report — July 2, 2026

## 1. Summary

Feed's basically dark today, every index and macro pull came back with a proxy 403 or "not enough data," so I can't tell you if the tape is risk-on or risk-off. The catch we're watching is that there's nothing to watch, zero gappers came through the scan, so there's no catalyst play to chase this morning.

## 2. Pre-Market Gappers

`gappers` is an empty list in packet.json. No tickers cleared the scan params (gap over 4 percent, price over 3 dollars, top 12). Nothing to report, no headlines to pull.

## 3. Day Trading Watchlist

Reminder on the rule this list encodes: **DAY watchlist = every gapper with `day_eligible: true`**, which is the Trend Join Long setup — gap over 3 percent, price over 3 dollars, market cap over 1 billion, premarket RVOL over 1.5, and price breaking above yesterday's high.

| Ticker | Catalyst | Levels | Plan | Conviction |
|---|---|---|---|---|
| — | — | — | — | — |

No gappers in the packet means no candidates cleared this flag. List is empty.

## 4. Swing Watchlist

Reminder on this rule too: **SWING watchlist = every gapper with `swing_eligible: true`**, meaning gap of 8 percent or more, price over 3 dollars, open above yesterday's high, open above the 200 day SMA, market cap of 800 million or more, and a real catalyst.

| Ticker | Catalyst | Theme | Trend | Conviction |
|---|---|---|---|---|
| — | — | — | — | — |

Same story, empty gapper list, empty watchlist.

## 5. Market Trends of the Day

Can't call it. Every index in `market_snapshot` (S&P 500, Dow, Nasdaq, Russell 2000, VIX, US 10Y, US 3M, WTI Oil, Dollar) came back with an error. S&P and Dow choked on a proxy CONNECT tunnel failure (403), everything else logged "not enough data." I'm not going to guess at a risk-on or risk-off tape with nothing behind it.

## 6. Technical Signals for Today

No data to work with here either, `gaps_to_fill` flags that intraday levels depend on yfinance 5 minute bars which can be thin or missing outside market hours, and with zero gappers there are no levels to even check. Nothing to report.

## 7. Economic Data, Rates and the Fed

`econ_calendar.today` is empty, and there's an explicit error note attached: the live fetch to the ForexFactory calendar failed with no cache fallback (proxy 403 again). So this isn't a light data day by coincidence, the feed was straight up unavailable. Not going to guess what's on deck.

## 8. Coming Up

`econ_calendar.tomorrow` is also empty, same feed failure applies. And since there are no gappers, there are no earnings dates to check for tomorrow or beyond. Nothing queued that I can confirm.

## 9. Skips and Traps

No gappers came through the scan, so there's nothing to mark as a skip or a trap today. If the feed comes back online later in the session, worth rerunning the scan, because right now this report is basically a data outage notice with a template wrapped around it.
