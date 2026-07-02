#!/usr/bin/env python3
"""
deliver.py - email an HTML premarket report via Resend.

Usage: python deliver.py reports/premarket_<date>.html

Reads RESEND_API_KEY and EMAIL_TO (and optional EMAIL_FROM) from a local
.env file next to this script. Real environment variables always win over
the .env file. No extra dependency, the .env parser and the HTTP POST both
use only the standard library.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date

DEFAULT_EMAIL_FROM = "AI Premarket Analyst <onboarding@resend.dev>"
RESEND_URL = "https://api.resend.com/emails"


def parse_env_file(path):
    values = {}
    if not os.path.exists(path):
        return values
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            values[key] = value
    return values


def get_config():
    here = os.path.dirname(os.path.abspath(__file__))
    file_values = parse_env_file(os.path.join(here, ".env"))

    def resolve(key, default=None):
        return os.environ.get(key) or file_values.get(key) or default

    return {
        "RESEND_API_KEY": resolve("RESEND_API_KEY"),
        "EMAIL_TO": resolve("EMAIL_TO"),
        "EMAIL_FROM": resolve("EMAIL_FROM", DEFAULT_EMAIL_FROM),
    }


def extract_report_date(path):
    match = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    if match:
        return match.group(1)
    return date.today().isoformat()


def send_email(api_key, email_to, email_from, subject, html_body):
    payload = json.dumps({
        "from": email_from,
        "to": [email_to],
        "subject": subject,
        "html": html_body,
    }).encode("utf-8")

    req = urllib.request.Request(
        RESEND_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode("utf-8")


def main():
    if len(sys.argv) < 2:
        print("Usage: python deliver.py reports/premarket_<date>.html")
        sys.exit(1)

    report_path = sys.argv[1]
    if not os.path.exists(report_path):
        print(f"Report file not found: {report_path}")
        sys.exit(1)

    config = get_config()

    if not config["RESEND_API_KEY"] or not config["EMAIL_TO"]:
        print("email skipped, set RESEND_API_KEY + EMAIL_TO")
        sys.exit(0)

    with open(report_path, "r") as f:
        html_body = f.read()

    report_date = extract_report_date(report_path)
    subject = f"AI Premarket Report - {report_date}"

    try:
        status, body = send_email(
            config["RESEND_API_KEY"],
            config["EMAIL_TO"],
            config["EMAIL_FROM"],
            subject,
            html_body,
        )
        print(f"Email sent to {config['EMAIL_TO']}, status {status}")
    except urllib.error.HTTPError as e:
        print(f"Resend request failed: {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        sys.exit(1)
    except Exception as e:
        print(f"Resend request failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
