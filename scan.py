#!/usr/bin/env python3
"""
scan.py - premarket data gatherer.

Collects raw premarket data into packet.json. Zero analysis happens here.
No conviction, no buckets, no opinions. All judgment happens later in AI
prompts. This file is only the source of truth for what was observed.

Uses only free, keyless libraries: yfinance, feedparser, requests.
zoneinfo is stdlib.
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import feedparser
import requests
import yfinance as yf

ET = ZoneInfo("America/New_York")
USER_AGENT = "Mozilla/5.0 (compatible; scan.py/1.0)"

# ---------- constants ----------

MARKET_SNAPSHOT_INSTRUMENTS = {
    "S&P 500": "^GSPC",
    "Dow": "^DJI",
    "Nasdaq": "^IXIC",
    "Russell 2000": "^RUT",
    "VIX": "^VIX",
    "US 10Y": "^TNX",
    "US 3M": "^IRX",
    "WTI Oil": "CL=F",
    "Dollar (DXY)": "DX-Y.NYB",
}

STATIC_UNIVERSE = [
    "NVDA", "AMD", "AVGO", "SMCI", "MRVL", "TSLA", "AAPL", "MSFT", "META", "AMZN",
    "GOOGL", "NFLX", "DELL", "SNOW", "PLTR", "COIN", "MSTR", "SOFI", "RIVN", "NIO",
    "MARA", "RIOT", "BA", "DIS", "JPM", "BAC", "XOM", "CVX", "HOOD", "UBER",
    "CRWD", "PANW", "CELH", "LULU", "NKE", "CAVA", "DKNG", "ARM", "INTC", "MU",
]

GAP_MIN_PCT = 4.0
GAP_MIN_PRICE = 3.0
GAP_TOP_N = 12

RSS_FEEDS = {
    "MarketWatch Top": "http://feeds.marketwatch.com/marketwatch/topstories/",
    "MarketWatch RealTime": "http://feeds.marketwatch.com/marketwatch/realtimeheadlines/",
    "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Google News Markets": "https://news.google.com/rss/search?q=markets+OR+earnings+when:1d&hl=en-US&gl=US&ceid=US:en",
}

SPAM_PATTERNS = [
    re.compile(r"price prediction", re.IGNORECASE),
    re.compile(r"\b20\d\d-20\d\d\b"),
]

PRIMARY_PUBLISHERS = [
    "bloomberg", "reuters", "cnbc", "marketwatch", "barron", "yahoo finance",
    "wsj", "wall street journal",
]

# Generic name words that must never count as a company match on their own,
# because they cross-match unrelated firms (e.g. "Applied" hits both Applied
# Optoelectronics and Applied Digital). Only a token that is both 4+ letters
# and absent from this set is distinctive enough to identify one company.
NAME_STOP = {
    "the", "inc", "corp", "corporation", "holdings", "technologies", "technology",
    "group", "digital", "applied", "advanced", "strategy", "strategies", "motors",
    "energy", "platforms", "industries", "international", "systems", "solutions",
    "global", "enterprises", "co", "company", "labs", "laboratories", "networks",
    "ventures", "partners", "capital", "financial",
}

ECON_CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
ECON_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".econ_calendar_cache.json")
ECON_CACHE_TTL_SECONDS = 4 * 60 * 60

HTML_TAG_RE = re.compile(r"<[^>]+>")


# ---------- market snapshot ----------

def get_market_snapshot():
    print("Fetching market snapshot...")
    snapshot = {}
    for name, symbol in MARKET_SNAPSHOT_INSTRUMENTS.items():
        try:
            hist = yf.Ticker(symbol).history(period="5d", interval="1d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                snapshot[name] = {"symbol": symbol, "error": "not enough data"}
                continue
            last = float(closes.iloc[-1])
            prev_close = float(closes.iloc[-2])
            change_pct = (last - prev_close) / prev_close * 100 if prev_close else None
            snapshot[name] = {
                "symbol": symbol,
                "last": round(last, 2),
                "prev_close": round(prev_close, 2),
                "change_pct": round(change_pct, 2) if change_pct is not None else None,
            }
        except Exception as e:
            print(f"  snapshot failed for {name} ({symbol}): {e}")
            snapshot[name] = {"symbol": symbol, "error": str(e)}
    return snapshot


# ---------- movers ----------

def fetch_screener(name):
    try:
        result = yf.screen(name)
        quotes = result.get("quotes", []) if isinstance(result, dict) else []
        return quotes
    except Exception as e:
        print(f"  screener '{name}' failed: {e}")
        return []


def get_live_movers():
    print("Fetching live top movers (day_gainers, most_actives)...")
    quotes = fetch_screener("day_gainers") + fetch_screener("most_actives")
    seen = {}
    for q in quotes:
        symbol = q.get("symbol")
        if not symbol or symbol in seen:
            continue
        gap_pct = q.get("regularMarketChangePercent")
        seen[symbol] = {
            "ticker": symbol,
            "name": q.get("shortName") or q.get("longName") or symbol,
            "price": q.get("regularMarketPrice"),
            "prev_close": q.get("regularMarketPreviousClose"),
            "gap_pct": round(gap_pct, 2) if gap_pct is not None else None,
            "market_cap": q.get("marketCap"),
            "volume": q.get("regularMarketVolume"),
        }
    return list(seen.values())


def get_static_universe_movers():
    print("Live screeners returned too few names, falling back to static universe...")
    movers = []
    for symbol in STATIC_UNIVERSE:
        try:
            tk = yf.Ticker(symbol)
            hist = tk.history(period="5d", interval="1d")
            closes = hist["Close"].dropna()
            if len(closes) < 2:
                continue
            last = float(closes.iloc[-1])
            prev_close = float(closes.iloc[-2])
            gap_pct = (last - prev_close) / prev_close * 100 if prev_close else None
            info = {}
            try:
                info = tk.info or {}
            except Exception:
                info = {}
            movers.append({
                "ticker": symbol,
                "name": info.get("shortName") or info.get("longName") or symbol,
                "price": round(last, 2),
                "prev_close": round(prev_close, 2),
                "gap_pct": round(gap_pct, 2) if gap_pct is not None else None,
                "market_cap": info.get("marketCap"),
                "volume": info.get("volume") or info.get("regularMarketVolume"),
            })
        except Exception as e:
            print(f"  static universe lookup failed for {symbol}: {e}")
    return movers


def get_movers():
    live = get_live_movers()
    if len(live) >= 5:
        return live, "live_screeners"
    static = get_static_universe_movers()
    return static, "static_universe"


def filter_gappers(movers):
    print("Filtering movers by gap percent and price...")
    filtered = []
    for m in movers:
        gap = m.get("gap_pct")
        price = m.get("price")
        if gap is None or price is None:
            continue
        if abs(gap) >= GAP_MIN_PCT and price >= GAP_MIN_PRICE:
            filtered.append(m)
    filtered.sort(key=lambda m: abs(m["gap_pct"]), reverse=True)
    return filtered[:GAP_TOP_N]


# ---------- market news ----------

def strip_html(text):
    if not text:
        return ""
    text = HTML_TAG_RE.sub("", text)
    return " ".join(text.split())


def is_spam(title):
    return any(p.search(title) for p in SPAM_PATTERNS)


def get_market_news():
    print("Fetching market wide news from RSS feeds...")
    items = []
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = getattr(entry, "title", "").strip()
                if not title or is_spam(title):
                    continue
                summary = strip_html(getattr(entry, "summary", "") or getattr(entry, "description", ""))
                items.append({
                    "source": source,
                    "title": title,
                    "link": getattr(entry, "link", ""),
                    "published": getattr(entry, "published", "") or getattr(entry, "updated", ""),
                    "published_parsed": getattr(entry, "published_parsed", None),
                    "summary": summary,
                })
        except Exception as e:
            print(f"  RSS feed '{source}' failed: {e}")
    return items


def top_n_news(items, n=20):
    def sort_key(item):
        pp = item.get("published_parsed")
        return time.mktime(pp) if pp else 0

    ranked = sorted(items, key=sort_key, reverse=True)
    return [{k: v for k, v in i.items() if k != "published_parsed"} for i in ranked[:n]]


# ---------- economic calendar ----------

def load_econ_cache():
    try:
        if os.path.exists(ECON_CACHE_FILE):
            with open(ECON_CACHE_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"  econ cache read failed: {e}")
    return None


def save_econ_cache(data):
    try:
        with open(ECON_CACHE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"  econ cache write failed: {e}")


def fetch_econ_raw():
    cache = load_econ_cache()
    now = datetime.now(ET)
    if cache and cache.get("fetched_at"):
        try:
            fetched_dt = datetime.fromisoformat(cache["fetched_at"])
            age = (now - fetched_dt).total_seconds()
            if age < ECON_CACHE_TTL_SECONDS:
                return cache.get("data"), None
        except Exception:
            pass
    try:
        resp = requests.get(ECON_CALENDAR_URL, headers={"User-Agent": USER_AGENT}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        save_econ_cache({"fetched_at": now.isoformat(), "data": data})
        return data, None
    except Exception as e:
        print(f"  econ calendar live fetch failed: {e}")
        if cache and cache.get("data"):
            return cache.get("data"), "live fetch failed, using cached week"
        return None, f"live fetch failed and no cache available: {e}"


def get_econ_calendar():
    print("Fetching economic calendar...")
    now_et = datetime.now(ET)
    today_date = now_et.date()
    tomorrow_date = today_date + timedelta(days=1)
    result = {
        "source": ECON_CALENDAR_URL,
        "filter": "country USD, impact High",
        "today_date": today_date.isoformat(),
        "tomorrow_date": tomorrow_date.isoformat(),
        "today": [],
        "tomorrow": [],
    }
    try:
        raw, note = fetch_econ_raw()
        if note:
            result["note"] = note
        if not raw:
            result["note"] = result.get("note") or "no data available"
            return result

        today_events = []
        tomorrow_events = []
        for event in raw:
            try:
                country = str(event.get("country", "")).strip().upper()
                impact = str(event.get("impact", "")).strip().lower()
                if country != "USD" or impact != "high":
                    continue
                date_str = event.get("date")
                if not date_str:
                    continue
                dt = datetime.fromisoformat(date_str)
                dt_et = dt.astimezone(ET) if dt.tzinfo else dt.replace(tzinfo=ET)
                record = {
                    "time_et": dt_et.strftime("%H:%M"),
                    "title": event.get("title", ""),
                    "forecast": event.get("forecast", ""),
                    "previous": event.get("previous", ""),
                }
                if dt_et.date() == today_date:
                    today_events.append((dt_et, record))
                elif dt_et.date() == tomorrow_date:
                    tomorrow_events.append((dt_et, record))
            except Exception as e:
                print(f"  skipping econ event due to error: {e}")

        today_events.sort(key=lambda x: x[0])
        tomorrow_events.sort(key=lambda x: x[0])
        result["today"] = [r for _, r in today_events]
        result["tomorrow"] = [r for _, r in tomorrow_events]
        return result
    except Exception as e:
        print(f"  economic calendar failed entirely: {e}")
        result["note"] = f"failed: {e}"
        return result


# ---------- catalyst headlines ----------

def build_name_tokens(company_name):
    if not company_name:
        return []
    tokens = re.findall(r"[A-Za-z]+", company_name)
    return [t for t in tokens if len(t) >= 4 and t.lower() not in NAME_STOP]


def headline_matches_ticker(text, ticker, name_tokens):
    if not text:
        return False
    if re.search(rf"\b{re.escape(ticker)}\b", text):
        return True
    for token in name_tokens:
        if re.search(rf"\b{re.escape(token)}\b", text, re.IGNORECASE):
            return True
    return False


def publisher_rank(publisher):
    if not publisher:
        return 99
    p = publisher.lower()
    for i, name in enumerate(PRIMARY_PUBLISHERS):
        if name in p:
            return i
    return 99


def get_catalyst_headlines(ticker, company_name, rss_items):
    headlines = []
    name_tokens = build_name_tokens(company_name)

    try:
        tk_news = yf.Ticker(ticker).news or []
        for item in tk_news:
            content = item.get("content", item)
            title = content.get("title") or item.get("title")
            if not title:
                continue
            publisher = None
            if isinstance(content.get("provider"), dict):
                publisher = content["provider"].get("displayName")
            publisher = publisher or item.get("publisher")
            link = None
            if isinstance(content.get("canonicalUrl"), dict):
                link = content["canonicalUrl"].get("url")
            link = link or item.get("link")
            headlines.append({
                "title": title,
                "publisher": publisher or "",
                "link": link or "",
                "source": "yfinance",
            })
    except Exception as e:
        print(f"    yfinance news failed for {ticker}: {e}")

    for entry in rss_items:
        title = entry.get("title", "")
        summary = entry.get("summary", "")
        if headline_matches_ticker(title, ticker, name_tokens) or headline_matches_ticker(summary, ticker, name_tokens):
            headlines.append({
                "title": title,
                "publisher": entry.get("source", ""),
                "link": entry.get("link", ""),
                "source": "rss",
            })

    seen_titles = set()
    deduped = []
    for h in headlines:
        key = h["title"].strip().lower()
        if key in seen_titles:
            continue
        seen_titles.add(key)
        deduped.append(h)

    deduped.sort(key=lambda h: publisher_rank(h["publisher"]))
    catalyst_found = len(deduped) > 0
    return deduped[:5], catalyst_found


# ---------- price levels ----------

def get_intraday_levels(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="1d", interval="5m", prepost=True)
        if hist.empty:
            return {"error": "no intraday data"}

        idx = hist.index
        idx = idx.tz_localize(ET) if idx.tz is None else idx.tz_convert(ET)
        hist = hist.copy()
        hist.index = idx

        market_open = datetime.now(ET).replace(hour=9, minute=30, second=0, microsecond=0)
        regular = hist[hist.index >= market_open]
        premarket = hist[hist.index < market_open]

        hod = float(regular["High"].max()) if not regular.empty else None
        lod = float(regular["Low"].min()) if not regular.empty else None
        premarket_high = float(premarket["High"].max()) if not premarket.empty else None
        premarket_volume = float(premarket["Volume"].sum()) if not premarket.empty else 0.0

        vwap = None
        total_volume = float(hist["Volume"].sum())
        if total_volume > 0:
            typical_price = (hist["High"] + hist["Low"] + hist["Close"]) / 3
            vwap = float((typical_price * hist["Volume"]).sum() / total_volume)

        return {
            "vwap": round(vwap, 2) if vwap is not None else None,
            "hod": round(hod, 2) if hod is not None else None,
            "lod": round(lod, 2) if lod is not None else None,
            "premarket_high": round(premarket_high, 2) if premarket_high is not None else None,
            "premarket_volume": int(premarket_volume),
        }
    except Exception as e:
        print(f"    intraday levels failed for {ticker}: {e}")
        return {"error": str(e)}


def get_daily_metrics(ticker):
    try:
        hist = yf.Ticker(ticker).history(period="1y", interval="1d")
        if hist.empty:
            return {"error": "no daily data"}

        idx = hist.index
        idx = idx.tz_localize(ET) if idx.tz is None else idx.tz_convert(ET)
        hist = hist.copy()
        hist.index = idx

        today_et = datetime.now(ET).date()
        past = hist[hist.index.date < today_et]
        today_row = hist[hist.index.date == today_et]

        if past.empty:
            return {"error": "not enough daily history"}

        sma_200 = float(past["Close"].tail(200).mean())
        prior_close = float(past["Close"].iloc[-1])
        prior_high = float(past["High"].iloc[-1])
        avg_volume_20 = float(past["Volume"].tail(20).mean())
        today_open = float(today_row["Open"].iloc[0]) if not today_row.empty else None

        return {
            "sma_200": round(sma_200, 2),
            "prior_day_high": round(prior_high, 2),
            "prior_close": round(prior_close, 2),
            "today_open": round(today_open, 2) if today_open is not None else None,
            "avg_volume_20d": int(avg_volume_20),
        }
    except Exception as e:
        print(f"    daily metrics failed for {ticker}: {e}")
        return {"error": str(e)}


def compute_rvol(today_volume, avg_volume_20d):
    if not today_volume or not avg_volume_20d:
        return None
    return round(today_volume / avg_volume_20d, 2)


def get_next_earnings_date(ticker):
    try:
        tk = yf.Ticker(ticker)
        cal = tk.get_earnings_dates(limit=8)
        if cal is not None and not cal.empty:
            idx = cal.index
            idx = idx.tz_localize(ET) if idx.tz is None else idx.tz_convert(ET)
            cal = cal.copy()
            cal.index = idx
            now_et = datetime.now(ET)
            future = cal[cal.index >= now_et]
            if not future.empty:
                return future.index.min().date().isoformat()
            return cal.index.max().date().isoformat()
        return None
    except Exception as e:
        print(f"    earnings date lookup failed for {ticker}: {e}")
        return None


# ---------- eligibility flags ----------

def compute_eligibility(gapper, daily_metrics, catalyst_found):
    gap = gapper.get("gap_pct")
    price = gapper.get("price")
    market_cap = gapper.get("market_cap")
    rvol = gapper.get("rvol")
    prior_high = daily_metrics.get("prior_day_high")
    sma_200 = daily_metrics.get("sma_200")
    today_open = daily_metrics.get("today_open")

    day_eligible = all([
        gap is not None and gap > 3,
        price is not None and price > 3,
        market_cap is not None and market_cap > 1_000_000_000,
        rvol is not None and rvol > 1.5,
        price is not None and prior_high is not None and price > prior_high,
    ])

    swing_eligible = all([
        gap is not None and gap >= 8,
        price is not None and price > 3,
        today_open is not None and prior_high is not None and today_open > prior_high,
        today_open is not None and sma_200 is not None and today_open > sma_200,
        market_cap is not None and market_cap >= 800_000_000,
        catalyst_found,
    ])

    return day_eligible, swing_eligible


# ---------- per gapper enrichment ----------

def build_gapper_record(mover, rss_items):
    ticker = mover["ticker"]
    print(f"Enriching {ticker}...")

    headlines, catalyst_found = get_catalyst_headlines(ticker, mover.get("name"), rss_items)
    intraday = get_intraday_levels(ticker)
    daily = get_daily_metrics(ticker)

    # yfinance reports about 0 premarket volume on the regular volume field,
    # so a true premarket RVOL needs a premarket feed (e.g. Alpaca).
    # Full-day relative volume below is the keyless stand-in.
    avg_vol_20 = daily.get("avg_volume_20d") if isinstance(daily, dict) else None
    rvol = compute_rvol(mover.get("volume"), avg_vol_20)

    next_earnings = get_next_earnings_date(ticker)

    gapper_for_flags = dict(mover)
    gapper_for_flags["rvol"] = rvol
    day_eligible, swing_eligible = compute_eligibility(
        gapper_for_flags, daily if isinstance(daily, dict) else {}, catalyst_found
    )

    record = dict(mover)
    record["rvol"] = rvol
    record["catalyst_headlines"] = headlines
    record["catalyst_found"] = catalyst_found
    record["intraday_levels"] = intraday
    record["daily_metrics"] = daily
    record["next_earnings_date"] = next_earnings
    record["day_eligible"] = day_eligible
    record["swing_eligible"] = swing_eligible
    return record


# ---------- main ----------

def main():
    generated_at = datetime.now(ET).isoformat()
    print("Starting premarket scan...")

    market_snapshot = get_market_snapshot()

    movers, candidate_source = get_movers()
    print(f"Candidate source: {candidate_source}, {len(movers)} raw candidates")

    gappers_basic = filter_gappers(movers)
    print(f"{len(gappers_basic)} names passed the gap filter")

    market_news_raw = get_market_news()
    market_news = top_n_news(market_news_raw, 20)

    econ_calendar = get_econ_calendar()

    gappers = []
    for mover in gappers_basic:
        try:
            gappers.append(build_gapper_record(mover, market_news_raw))
        except Exception as e:
            print(f"  failed to build record for {mover.get('ticker')}: {e}")

    packet = {
        "generated_at": generated_at,
        "candidate_source": candidate_source,
        "trading_day_note": (
            "Market snapshot uses the last two daily closes. Premarket RVOL is a "
            "full-day stand-in, see gaps_to_fill."
        ),
        "scan_params": {
            "gap_min_pct": GAP_MIN_PCT,
            "gap_min_price": GAP_MIN_PRICE,
            "gap_top_n": GAP_TOP_N,
        },
        "criteria": {
            "day_trading": (
                "Trend Join Long. Gap vs prev close over 3 percent, price over 3 dollars, "
                "market cap over 1 billion, premarket RVOL over 1.5, price breaking above "
                "yesterday's high."
            ),
            "swing": (
                "Gap of 8 percent or more, price over 3 dollars, open above yesterday's high, "
                "open above the 200 day SMA, market cap of 800 million or more, and a real catalyst."
            ),
        },
        "market_snapshot": market_snapshot,
        "econ_calendar": econ_calendar,
        "gappers": gappers,
        "market_news": market_news,
        "gaps_to_fill": [
            "Market wide earnings calendar is partial, only a next earnings date per gapper "
            "is pulled, not a full market earnings sheet.",
            "Intraday levels (VWAP, HOD, LOD, premarket high) depend on yfinance 5 minute bars "
            "and can be thin or missing outside market hours.",
            "RVOL here is full-day volume over the 20 day average volume, not true premarket "
            "RVOL, because yfinance premarket volume is unreliable.",
        ],
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "packet.json")
    with open(out_path, "w") as f:
        json.dump(packet, f, indent=2, default=str)

    print(f"Done. Wrote {out_path}")


if __name__ == "__main__":
    main()
