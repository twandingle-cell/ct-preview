#!/usr/bin/env python3
"""
render_html.py - convert the merged premarket report to an emailable HTML file.

Usage: python render_html.py REPORT.md
Writes: reports/premarket_<date>.html
"""

import os
import re
import sys
from datetime import date
from zoneinfo import ZoneInfo
from datetime import datetime

import markdown

ET = ZoneInfo("America/New_York")

PAGE_TEMPLATE = """<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <style>
      body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; color: #1a1a1a; max-width: 720px; margin: 0 auto; padding: 24px; line-height: 1.5; }}
      h1 {{ font-size: 22px; }}
      h2 {{ font-size: 18px; margin-top: 28px; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px; }}
      h3 {{ font-size: 14px; color: #4b5563; font-weight: 600; margin: 4px 0; }}
      blockquote {{ background: #f8fafc; border-left: 3px solid #94a3b8; margin: 12px 0; padding: 8px 14px; color: #475569; font-size: 13px; }}
      table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }}
      th, td {{ border: 1px solid #e5e7eb; padding: 6px 10px; text-align: left; vertical-align: top; }}
      th {{ background: #f8fafc; }}
      hr {{ border: none; border-top: 1px solid #e5e7eb; margin: 24px 0; }}
      code {{ background: #f1f5f9; padding: 1px 4px; border-radius: 3px; }}
    </style>
  </head>
  <body>
{body}
  </body>
</html>
"""


def extract_report_date(markdown_text):
    match = re.search(r"(\d{4}-\d{2}-\d{2})", markdown_text)
    if match:
        return match.group(1)
    return datetime.now(ET).date().isoformat()


def extract_title(markdown_text):
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "AI Premarket Report"


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_html.py REPORT.md")
        sys.exit(1)

    report_path = sys.argv[1]
    if not os.path.exists(report_path):
        print(f"Report file not found: {report_path}")
        sys.exit(1)

    with open(report_path, "r") as f:
        markdown_text = f.read()

    body_html = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    title = extract_title(markdown_text)
    page_html = PAGE_TEMPLATE.format(title=title, body=body_html)

    report_date = extract_report_date(markdown_text)
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "reports")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"premarket_{report_date}.html")

    with open(out_path, "w") as f:
        f.write(page_html)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
